from django.urls import path
from . import views
from .views import  UserRegistrationView,GetRoutesView,UserProfileView,UserProfileCreateView #UserTokenView AdminTokenObtainPairView
from .views import CustomTokenObtainPairView, CustomTokenRefreshView,UserListView,BlockUnblockUserView,UserDetailView,UserProfileUpdateView
    
from .views import  ForgotPasswordView,ForgotPasswordOTPView,UserChangePasswordView
from .views import SendOTP, VerifyOTP

urlpatterns = [
    
    path('',views.GetRoutesView.as_view(),name='getRoutes'),
    path('user/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('admin/users/', UserListView.as_view(), name='user-list'),
    path('admin/block-unblock/<int:pk>/', BlockUnblockUserView.as_view(), name='block-unblock-user'),
    path('user/user-profile/<int:user_id>', UserProfileView.as_view(), name='user-profile'),
    path('user/detail-view/<int:user_id>/',UserDetailView.as_view(), name='user-detail'),
    path('user/add-profile/<int:user_id>', UserProfileCreateView.as_view(), name='user-profile-create'),
    path('user/update-profile/<int:user_id>', UserProfileUpdateView.as_view(), name='user-updation'),


    path('send-otp/', SendOTP.as_view(), name='send_otp'),
    path('verify-otp/<int:phone>',VerifyOTP.as_view(), name='verify_otp'),
    # Other URL patterns...


    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('forgot-password-otp/', ForgotPasswordOTPView.as_view(), name='forgot-password-otp'),
    # path('reset-password-confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password-reset'),
    path('change-password/', UserChangePasswordView.as_view(), name='change-password'),
   

    # path('user/reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    # path('user/forgot-password/', ForgotPasswordAPIView.as_view(), name='reset-password'),
    # path('user/send-otp/', EmailOTPVerificationView.as_view(), name='send_otp'),

    # Chat/Text Messaging Functionality







]
    
    
    
    
    
    
    
    
    
    
    
    
 


    


