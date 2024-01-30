import re
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.humanize.templatetags import humanize
from .models import Role,AccountUser,UserProfile
from django.utils.timesince import timesince
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from accounts.utils import Util
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.hashers import check_password

# user register serializer

User = get_user_model()

#<-----------------------User Side--------------------------->

class UserRegisterSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(
        required = True,
        validators = [UniqueValidator(queryset=User.objects.all())]
    )

    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset=User.objects.all())]
    )
    
    phone_number = serializers.CharField(
        required = True,
        validators = [UniqueValidator(queryset=User.objects.all(),message = "Phone number already exists"),]
    )

    password = serializers.CharField(write_only=True,required = True)
    password2 = serializers.CharField(write_only=True,required = True)

    class Meta:
        model = User
        fields = ['first_name','email','phone_number','password','password2']

    def validate_password(self, password):
        # Password policy: Minimum 6 characters, at least one uppercase letter, one lowercase letter, and one digit
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{6,}$', password):
            raise serializers.ValidationError(
                "Password must be at least 6 characters long and contain at least one uppercase letter, one lowercase letter, and one digit."
            )
        return password

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        phone_number = attrs.get('phone_number', None)
        if phone_number:
            # Define a regex pattern for a standard phone number format (adjust as needed)
            phone_number_pattern = r'^\d{10}$'
            # Check if the phone number matches the pattern
        if not re.match(phone_number_pattern, phone_number):
                raise serializers.ValidationError({"phone_number": "Invalid phone number format. Must be a 10-digit number."})
        return attrs
    
    def create(self, validated_data):
        print("user serializer", validated_data)
        

        user = User.objects.create(
            first_name = validated_data['first_name'],
            email = validated_data['email'],
            phone_number = validated_data['phone_number']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod    
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email  # Assuming you have a 'role' field in your user model
        token['phone_number'] = str(user.phone_number)
        token['first_name'] = user.first_name
        return token

class CustomTokenRefreshSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['access'] = str(refresh.access_token)
        data['email'] = self.user.email
        data['phone_number'] = self.user.phone_number
        data['first_name'] = self.user.first_name
        return data


class UserProfileSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(queryset=AccountUser.objects.all())

    class Meta:
        model = UserProfile
        fields = ['user','name','address','city', 'state', 'country']

#<-------------------User Side End-------------->

#<---------------Admin Side------------------>

class UserSerializer(serializers.ModelSerializer):

    date_joined = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    last_login_display = serializers.SerializerMethodField()

    class Meta:
        model = AccountUser
        fields = ['id','first_name','email','phone_number','is_active','is_superuser','image','date_joined','last_login_display']

    def get_last_login_display(self, obj):
        return humanize.naturaltime(obj.last_login)



class ForgotPasswordSerializer(serializers.Serializer):
    mobile_number = serializers.CharField()
    otp = serializers.CharField(max_length=6)



class UserChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(max_length =255,style = {'input_type':'password'},write_only = True)
    new_password = serializers.CharField(max_length =255,style = {'input_type':'password'},write_only = True)
    new_password2 = serializers.CharField(max_length =255,style = {'input_type':'password'},write_only = True)

    class Meta:
        model = AccountUser
        fields = ['old_password','new_password','new_password2']

    def validate(self, attrs):

        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        new_password2 = attrs.get('new_password2')
        user = self.context.get('user')

      

        if not check_password(old_password,user.password):
            raise serializers.ValidationError("Old Password and Entered Password Doesn't Match")
            
        if new_password != new_password2:
            raise serializers.ValidationError("password doesn't match")
        user.set_password(new_password)
        user.save()
        return attrs
  

class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


class GetUserSerializer(serializers.ModelSerializer):
     class Meta:
        model = AccountUser
        fields = '__all__'







    


    

    

#<--------------Admin Side End------------------------->


#<------------------Chat Starts------------------------->



#<----------------------Chat Ends------------------------------------>


# class ProfileSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Profile
#         fields = [ 'id',  'user',  'full_name', 'image' ]
    
#     def __init__(self, *args, **kwargs):
#         super(ProfileSerializer, self).__init__(*args, **kwargs)
#         request = self.context.get('request')
#         if request and request.method=='POST':
#             self.Meta.depth = 0
#         else:
#             self.Meta.depth = 3


# class MessageSerializer(serializers.ModelSerializer):
#     reciever_profile = ProfileSerializer(read_only=True)
#     sender_profile = ProfileSerializer(read_only=True)

#     class Meta:
#         model = ChatMessage
#         fields = ['id','sender', 'reciever', 'reciever_profile', 'sender_profile' ,'message', 'is_read', 'date']
    
#     def __init__(self, *args, **kwargs):
#         super(MessageSerializer, self).__init__(*args, **kwargs)
#         request = self.context.get('request')
#         if request and request.method=='POST':
#             self.Meta.depth = 0
#         else:
#             self.Meta.depth = 2