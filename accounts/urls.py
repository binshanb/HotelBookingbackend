from django.urls import path
from . import views
from .views import  UserRegistrationView,GetRoutesView,UserProfileView,AddProfileAPIView #UserTokenView AdminTokenObtainPairView
from .views import CustomTokenObtainPairView, CustomTokenRefreshView,UserListView,BlockUnblockUserView,UserProfileDetailView,EditProfileAPIView
    
from .views import  ForgotPasswordView,ForgotPasswordOTPView,ResetPasswordAPIView,UserChangePasswordView,EmailVerificationFailed,VerifyEmail
from .views import OtpSent, OtpVerify

urlpatterns = [
    
    path('',views.GetRoutesView.as_view(),name='getRoutes'),
    path('user/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('admin/users/', UserListView.as_view(), name='user-list'),
    path('user/verify-email/',VerifyEmail.as_view(),name ="register"),
    path('user/verify-email-fail/',EmailVerificationFailed.as_view(),name ="register"),
    path('admin/block-unblock/<int:pk>/', BlockUnblockUserView.as_view(), name='block-unblock-user'),
    path('user/user-profile/<int:pk>', UserProfileView.as_view(), name='user-profile'),
    path('user/detail-view/<int:pk>/',UserProfileDetailView.as_view(), name='user-detail'),
    path('user/add-profile/', AddProfileAPIView.as_view(), name='add-profile'),
    path('user/edit-profile/<int:user_id>/', EditProfileAPIView.as_view(), name='update-profile'),
    # other URL patterns...    path('user/update-profile/<int:user_id>', UserProfileUpdateView.as_view(), name='user-updation'),

    path('sent-otp/',OtpSent.as_view(),name='sentotp'),
    path('verify-otp/',OtpVerify.as_view(),name='verifyotp'),
    # Other URL patterns...


    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('forgot-password-otp/', ForgotPasswordOTPView.as_view(), name='forgot-password-otp'),
    path('change-password/', UserChangePasswordView.as_view(), name='change-password'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset_password'),

   
   

    # Chat/Text Messaging Functionality







]
    
    
    
    
    
    
    
    
    
    
    
    
 


    


