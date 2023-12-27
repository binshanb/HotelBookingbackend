from django.shortcuts import render
from rest_framework.response import Response
from django.db.models import Subquery,OuterRef,Q
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics,permissions
from rest_framework.generics import UpdateAPIView,RetrieveAPIView
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.urls import reverse
# from .utils import Util
from drf_yasg import openapi
import jwt
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserRegisterSerializer,UserChangePasswordSerializer,ForgotPasswordSerializer
from .serializers import CustomTokenObtainPairSerializer,CustomTokenRefreshSerializer,UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView ,TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import AccountUser
from .serializers import UserProfileSerializer
import random
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .renderers import AccountUserRenderer
from rest_framework.authtoken.models import Token

from .helper import send_otp,verify_otp
from . import helper

from twilio.rest import Client
from django.db import IntegrityError



User = get_user_model()


class GetRoutesView(APIView):
    def get(self, request):
        routes = [
            'api/token/user',
            'api/token/admin',
            'api/token/refresh/',
            'api/token/verify/',
            'api/user/register',
        
           
            
        ]

        return Response(routes)
    

#<---------------------------User Side-------------------->

class UserRegistrationView(APIView):

    def post(self,request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception = True):
            try:
                user = serializer.save()
                return Response(UserRegisterSerializer(user).data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"IntegrityError": True}, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['first_name'] = user.first_name
        token['is_superuser'] = user.is_superuser
        token['email'] = user.email
        token['role'] = user.role
        token['phone_number'] = user.phone_number

        print(token)
        return token

       
    
class MyTokenObtainPairView(TokenObtainPairView):
    
    serializer_class = MyTokenObtainPairSerializer

"""class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer
"""

#<------------------Admin Side------------------>


class UserListView(generics.ListAPIView):

    serializer_class = UserSerializer
    def get_queryset(self):
        
        return AccountUser.objects.filter(is_superuser = 'False')
    
class BlockUnblockUserView(UpdateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return AccountUser.objects.all()
    
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance:
            instance.is_active = not instance.is_active
            instance.save()

            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            return Response({"detail":"User not Found"},status=status.HTTP_404_NOT_FOUND)
        

#<------------------------------User Profile----------------------->

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class UserProfileCreateView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)


class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return AccountUser.objects.filter(user=self.request.user)
    

        
class UserDetailView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

    



class ForgotPasswordView(APIView):
    def post(self, request):
        mobile_number = request.data.get('phone_number')
        if not mobile_number:
            return Response({'error': 'You must enter a mobile number'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = AccountUser.objects.filter(phone_number=mobile_number)
        if user.exists():
            # Generate OTP and send it (assuming `verify.send` method does this)
            helper.send_otp('+91' + str(mobile_number))
            return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Mobile number does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
class ForgotPasswordOTPView(APIView):
    def post(self, request):
        mobile_number = request.data.get('phone_number')
        otp = request.data.get('otp')

        if not mobile_number or not otp:
            return Response({'error': 'Invalid request. Please provide mobile number and OTP.'}, status=status.HTTP_400_BAD_REQUEST)

        if helper.verify_otp('+91' + str(mobile_number), otp):
            try:
                user = AccountUser.objects.get(phone_number=mobile_number)
                if user:
                    return Response({'message': 'Redirect to reset password view'}, status=status.HTTP_200_OK)  # Modify this line as per your redirect logic
            except AccountUser.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)



class UserChangePasswordView(APIView):
    renderer_classes = [AccountUserRenderer]
    permission_classes =[IsAuthenticated]

    def post(self,request,format= None):
        serializer_class = UserChangePasswordSerializer(data = request.data,context ={'user':request.user})
        if serializer_class.is_valid(raise_exception=True):
            return Response({"msg":"password change successfull"},status=status.HTTP_200_OK)
        return Response(serializer_class.errors,status=status.HTTP_400_BAD_REQUEST)




    

class SendOTP(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'message': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

        sent = send_otp(phone_number)
        if sent:
            return Response({'message': 'OTP sent successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Failed to send OTP.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyOTP(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')
        if not phone_number or not otp:
            return Response({'message':'OTP code are required.'}, status=status.HTTP_400_BAD_REQUEST)

        verified =verify_otp (phone_number, otp)
        if verified:
            return Response({'message': 'OTP verified successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'OTP verification failed.'}, status=status.HTTP_400_BAD_REQUEST)


# class OtpSent(APIView):
#     # permission_classes=[IsAuthenticated]
#     def get(self,request):
#         print(request.user)
#         user = request.user
#         mobile = user.phone
#         if user:  #if user exists
#             helper.send('+91' + str(mobile))
#             return Response({'message':"success"},status=200)
#         else:
#             return Response({'message':"User Not Found"},status=401)
            

# class OtpVerify(APIView):
#     permission_classes=[IsAuthenticated]
#     def post(self, request):
#         # Extract 'otp' from the query parameters
     
#         otp = request.data.get('otp')
#         user = request.user
#         mobile = user.phone_number
#         print(mobile,otp)
#         if helper.check('+91' + str(mobile), otp):
#                 print(user,"this is user")
#                 return Response({'message':"succes"},status=200)
#         else:
#                 return Response({'message':"Invalid Otp"},status=400)




# class LoginWithOTP(APIView):
#     def post(self, request):
#         email = request.data.get('email', '')
#         try:
#             user = AccountUser.objects.get(email=email)
#         except AccountUser.DoesNotExist:
#             return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

#         otp = generate_otp()
#         user.otp = otp
#         user.save()

#         send_otp_email(email, otp)
#         # send_otp_phone(phone_number, otp)

#         return Response({'message': 'OTP has been sent to your email.'}, status=status.HTTP_200_OK)
    


# class ValidateOTP(APIView):
#     def post(self, request):
#         email = request.data.get('email', '')
#         otp = request.data.get('otp', '')

#         try:
#             user = AccountUser.objects.get(email=email)
#         except AccountUser.DoesNotExist:
#             return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

#         if user.otp == otp:
#             user.otp = None  # Reset the OTP field after successful validation
#             user.save()

#             # Authenticate the user and create or get an authentication token
#             token, _ = Token.objects.get_or_create(user=user)

#             return Response({'token': token.key}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)



























# class ResetPasswordAPIView(APIView):
#     def post(self, request):
#         serializer = ResetPasswordSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         email = serializer.validated_data.get('email')
#         new_password = serializer.validated_data.get('new_password')

#         # Retrieve the user based on the validated email
#         from .models import CustomUser  # Import your user model
#         user = CustomUser.objects.get(email=email)
        
#         # Reset the user's password
#         user.set_password(new_password)
#         user.save()

#         return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)



# class ForgotPasswordAPIView(APIView):

#     def post(self, request):
#         serializer =ForgotPasswordSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         email = serializer.validated_data.get('email')

#         user = AccountUser.objects.filter(email=email).first()
#         if user:
#             # Assuming send_email_verification_code is a function to send verification codes to emails
#             send_email_verification_code(email)  # Implement this function to send email verification codes

#             # You can also generate and return a session key or token if needed for subsequent steps

#             return Response({'message': 'Verification code sent successfully'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'message': 'Email address does not exist'}, status=status.HTTP_404_NOT_FOUND)


# class EmailOTPVerificationView(APIView):
#     def post(self, request):
#         serializer = EmailOTPSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         email = serializer.validated_data.get('email')

#         # Generate and send the email OTP
#         send_email_otp(email)  # Implement this function to send email OTP

#         return Response({'message': 'Email OTP sent successfully'}, status=status.HTTP_200_OK)
    























# class ContactListView(generics.ListAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = UserSerializer

#     def get_queryset(self):
#         current_user = self.request.user
#         following_query = Q(followers__follower=current_user)
#         followers_query = Q(following__following=current_user)
#         queryset = AccountUser.objects.filter(following_query | followers_query).exclude(id=current_user.id).distinct()
#         return queryset
    



    

# # Chat APp
# class MyInbox(generics.ListAPIView):
#     serializer_class = MessageSerializer

#     def get_queryset(self):
#         user_id = self.kwargs['user_id']

#         messages = ChatMessage.objects.filter(
#             id__in =  Subquery(
#                 AccountUser.objects.filter(
#                     Q(sender__reciever=user_id) |
#                     Q(reciever__sender=user_id)
#                 ).distinct().annotate(
#                     last_msg=Subquery(
#                         ChatMessage.objects.filter(
#                             Q(sender=OuterRef('id'),reciever=user_id) |
#                             Q(reciever=OuterRef('id'),sender=user_id)
#                         ).order_by('-id')[:1].values_list('id',flat=True) 
#                     )
#                 ).values_list('last_msg', flat=True).order_by("-id")
#             )
#         ).order_by("-id")
            
#         return messages
    
# class GetMessages(generics.ListAPIView):
#     serializer_class = MessageSerializer
    
#     def get_queryset(self):
#         sender_id = self.kwargs['sender_id']
#         reciever_id = self.kwargs['reciever_id']
#         messages =  ChatMessage.objects.filter(sender__in=[sender_id, reciever_id], reciever__in=[sender_id, reciever_id])
#         return messages

# class SendMessages(generics.CreateAPIView):
#     serializer_class = MessageSerializer



# class ProfileDetail(generics.RetrieveUpdateAPIView):
#     serializer_class = ProfileSerializer
#     queryset = Profile.objects.all()
#     permission_classes = [IsAuthenticated]  


# class SearchUser(generics.ListAPIView):
#     serializer_class = ProfileSerializer
#     queryset = Profile.objects.all()
#     permission_classes = [IsAuthenticated]  

#     def list(self, request, *args, **kwargs):
#         username = self.kwargs['username']
#         logged_in_user = self.request.user
#         users = Profile.objects.filter(Q(user__username__icontains=username) | Q(full_name__icontains=username) | Q(user__email__icontains=username) & 
#                                        ~Q(user=logged_in_user))

#         if not users.exists():
#             return Response(
#                 {"detail": "No users found."},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = self.get_serializer(users, many=True)
#         return Response(serializer.data)


















# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from rest_framework import permissions, status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.views import APIView
# from accounts.models import CustomUser
# from .serializers import UserRegisterSerializer, UserSerializer
# from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError
# from rest_framework.exceptions import AuthenticationFailed

# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView
# from django.db.models import Q


# from django.http import JsonResponse


# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):

#         print(user, "login side in server")
#         token = super().get_token(user)

#         # Add custom claims
        
#         token['email'] = user.email
#         token['name'] = user.name
#         token['is_superuser'] = user.is_superuser
#         print("serialissssss",user.image)
#         # token['image'] = user.image


#         # ...

#         return token


# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer


# # @api_view(['GET'])
# # def apiOverview(request):
# #     api_urls = {
# #         # admin-side
# #         'account-list': '/user-list/',
# #         # 'admin-user-create': '/user-create/',
# #         'admin-user-delete': '/user-delete/',
# #         'admin-user-update': '/user-update/',

# #         # user-side
# #         'user-create': '/user-create/',
# #         'user-profile': '/user-profile/',
# #         'user-add-img': '/user-add-img/',
# #         'user-edit-img': '/user-edit-img/',
# #     }
# #     return Response(api_urls)

# # class Loginview(APIView):
# #     def post(self, request):
# #         email = request.data["email"]
# #         password = request.data["password"]
# #         try:
# #             user = Account.objects.get(email = email)
# #         except Account.DoesNotExist:
# #             raise AuthenticationFailed("Account does  not exist")
# #         if user is None:
# #             raise AuthenticationFailed("User does not exist")
# #         if not user.check_password(password):
# #             raise AuthenticationFailed("Incorrect Password")
# #         access_token = AccessToken.for_user(user)
# #         refresh_token =RefreshToken.for_user(user)
# #         return Response({
# #             "access_token" : access_token,
# #             "refresh_token" : refresh_token
# #         })

# class RegisterView(APIView):
#     def post(self, request):
#         data = request.data
#         print(data)
#         serializer = UserRegisterSerializer(data=data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
# #currently authenticated user
# class UserView(APIView):
    
#     permission_classes = [permissions.IsAuthenticated]
#     def get(self, request):
#         user = request.user
#         serializer = UserSerializer(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class ImageUploadView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
    
#     def put(self, request, format=None):
#         print('image uploaded', request)
#         data = request.data["image"]
#         print("upload",data)
#         user = request.user
#         user.image = data
#         user.save()
#         serializer = UserSerializer(user)
#         return Response(serializer.data, status = status.HTTP_200_OK)
    
# class RegisteredUserView(APIView):
#     permission_classes = [permissions.IsAdminUser]
   
#     def get(self,request):
#         user = CustomUser.objects.exclude(is_superuser=True)
#         serializer = UserSerializer(user, many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)  
    
# class UpdateView(APIView):
#     permission_classes = [permissions.IsAdminUser]
#     def post(self, request, id):
#         user = CustomUser.objects.get(id = id)
#         user.name = request.data['name']
#         user.email = request.data['email']
#         user.save()
#         return Response({"message": "success"}, status = status.HTTP_200_OK)

# class DeleteView(APIView):
#     permission_classes = [permissions.IsAdminUser]
#     def get(self,request, id):
#         user = CustomUser.objects.get(id=id)
#         user.delete()
#         return Response({"message": "success"}, status = status.HTTP_200_OK)
    
# def search_users(request):
#     search_term = request.GET.get('q')

#     if search_term:
#         users = CustomUser.objects.exclude(is_superuser=True).filter(
#             Q(name__icontains=search_term) | Q(email__icontains=search_term)
#         )
#     else:
#         users = CustomUser.objects.exclude(is_superuser=True)

#     serializer = UserSerializer(users, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(['POST'])

# def block_user(request, email):
#     try:
#         user = CustomUser.objects.get(email=email)
#         user.is_block = True
#         user.save()
#         return JsonResponse({'message': 'User blocked successfully'})
#     except CustomUser.DoesNotExist:
#         return JsonResponse({'error': 'User not found'}, status=404)

# @api_view(['POST'])

# def unblock_user(request, email):
#     try:
#         user = CustomUser.objects.get(email=email)
#         user.is_block = False
#         user.save()
#         return JsonResponse({'message': 'User unblocked successfully'})
#     except CustomUser.DoesNotExist:
#         return JsonResponse({'error': 'User not found'}, status=404)


    