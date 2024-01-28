
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.generics import UpdateAPIView
from django.db.models import Q

 
from django.contrib.auth.hashers import check_password
import jwt
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserRegisterSerializer,UserChangePasswordSerializer
from .serializers import CustomTokenObtainPairSerializer,CustomTokenRefreshSerializer,UserSerializer,GetUserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView ,TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import AccountUser,UserProfile
from .serializers import UserProfileSerializer
import random





from .renderers import AccountUserRenderer
from rest_framework.authtoken.models import Token

from . import helper
from .email import *






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
    


            



class UserRegistrationView(APIView):
    renderer_classes = [AccountUserRenderer]
    permission_classes = [AllowAny]

    def post(self,request,format=None):
        copy = request.data
        otp = ''.join(random.choices('0123456789', k=4))
        copy['otp'] = otp
        copy['is_active'] = False
        
        serializer = UserRegisterSerializer(data=copy)
        
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()
            set_otp_via_email(serializer.data['email'])


            return Response({'msg':"reg sucess"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,{'msg':"extra "},status=status.HTTP_400_BAD_REQUEST)


    



class VerifyEmail(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = request.data
            email = data['email']
            otp = data['otp']

            try:
                user = AccountUser.objects.get(email=email)
            except AccountUser.DoesNotExist:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            if user and user.otp == otp:
                user.is_active = True
                user.save()
                return Response({"message": "Account Verified"}, status=status.HTTP_200_OK)
            else:
                # Handle the case when OTP verification fails
                user.is_active = False
                user.save()  # Save the user object after setting is_active to False
                return Response({"message": "Wrong Otp"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": f"Something went wrong: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationFailed(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            data = request.data
            email = data['email']
            print(email)
            user = AccountUser.objects.get(email = email)
            if user :
                user.delete()
                return Response({"message":"User poped out of table"},status=status.HTTP_200_OK)
            return Response({"message":"User not in table"},status=status.HTTP_200_OK)
        except:
            return Response({"message":"No got got from verify otp page"},status=status.HTTP_404_NOT_FOUND)
        

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


        
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

    def put(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AddProfileAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(data=request.data)
        print(serializer,"seriallll")
        if serializer.is_valid():
            serializer.save() 
            return Response("Profile details added", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


 
class EditProfileAPIView(APIView):
    def put(self, request, user_id, *args, **kwargs):
        try:
            user_profile = UserProfile.objects.get(user_id=user_id)  # Retrieve UserProfile based on user_id

            # Update the user profile with the data from the request
            user_profile.name = request.data.get('name', user_profile.name)
            user_profile.address = request.data.get('address', user_profile.address)
            user_profile.city = request.data.get('city', user_profile.city)
            user_profile.state = request.data.get('state', user_profile.state)
            user_profile.country = request.data.get('country', user_profile.country)

            # Save the updated user profile
            user_profile.save()

            return Response({'message': 'Profile details updated successfully'}, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'message': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'Error updating user profile: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

        
class UserProfileDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            user_profiles = UserProfile.objects.filter(user_id=pk)  # Retrieve UserProfile(s) based on user_id
            if user_profiles.exists():
                serializer = UserProfileSerializer(user_profiles, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except UserProfile.DoesNotExist:
            return Response({'message': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)


    



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


class ResetPasswordAPIView(APIView):
    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        new_password2 = request.data.get('new_password2')
        user = request.user  # Assuming the user is authenticated
        
        if not (old_password and new_password and new_password2):
            return Response({'message': 'All password fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(old_password):
            return Response({'message': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)
        
        if new_password != new_password2:
            return Response({'message': 'New passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        
        return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)

    

class OtpSent(APIView):
    def post(self, request):
        print(request, "reqqqqq")
        phone_number = request.data.get('phone_number')
        print(phone_number,"phone")
        try:
            user = AccountUser.objects.get(phone_number=phone_number)  # Retrieve user by phone number
            print(user,"User")
            if user:
               sid = helper.send_otp('+91' + str(phone_number))  # Send OTP via Twilio
            print(sid,"sid")
            if sid:
                return Response({'message': "OTP sent successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({'message': "Failed to send OTP."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except AccountUser.DoesNotExist:
            return Response({'message': "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error sending OTP: {e}")
            return Response({'message': "Failed to send OTP."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class OtpVerify(APIView):
  
    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')
        try:
            user = AccountUser.objects.get(phone_number=phone_number)  # Retrieve user by phone number
            print(user,"User")
            verification_status = helper.verify_otp('+91' + str(phone_number), otp)  # Verify OTP using Twilio

            if verification_status:
                return Response({'message': "OTP verification successful. User logged in."}, status=status.HTTP_200_OK)
            else:
                return Response({'message': "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
        except AccountUser.DoesNotExist:
            return Response({'message': "User not found."}, status=status.HTTP_404_NOT_FOUND)
        

class UserSearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query', None)

        if not query:
            return Response({'error': 'Query parameter "query" is required'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = AccountUser.objects.filter(
            Q(first_name__icontains=query) | Q(email__icontains=query)
        ).exclude(pk=request.user.id)

        serializer = GetUserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        

