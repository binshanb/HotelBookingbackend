from django.urls import path
# from . import views
from .views import *
urlpatterns = [

    path('admin/add-category/', CreateCategoryView.as_view(), name='add-category'),
    path('admin/room-category/<int:category_id>/', EditCategoryView.as_view(), name='update_category'),
    path('admin/room-category/block-unblock/<int:pk>/',BlockUnblockCategoryView.as_view(), name='block_ublock-category'),
    path('admin/room-category/', CategoryListView.as_view(), name='room-category'),
    path('category-list/',UserCategoryListAPIView.as_view(),name="user-category-list"),
    
    
    path('admin/edit-room/<int:room_id>/',EditRoomView.as_view(), name='edit-room'),
    path('admin/add-room/', CreateRoomView.as_view(), name='add-room'),
    path('admin/room-list/', RoomListView.as_view(), name='room-list'),
    path('admin/room-retrieve/<int:pk>/', RoomRetrieveUpdateDestroyView.as_view(), name='room-retrieve'),
    path('room-detail/<int:id>/', RoomDetailsView.as_view(), name='room-detail'),
    path('roomlistuser/', RoomListUserView.as_view(), name='room-list-user'),
    path('admin/room-list/block-unblock/<int:pk>/',BlockUnblockRoomView.as_view(), name='block_ublock-room'),
    path('admin/dashboard-data/', DashboardDataAPIView.as_view(), name='dashboard-data'),

    
    path('admin/edit-feature/<int:id>/',EditRoomFeatureView.as_view(), name='edit-feature'),
    path('admin/add-feature/', CreateRoomFeatureView.as_view(), name='add-feature'),
    path('admin/room-feature/', RoomFeatureView.as_view(), name='room-feature'),
    path('admin/room-feature/block-unblock/<int:pk>/', BlockUnblockRoomFeatureView.as_view(), name='block_ublock-feature'),
    path('get-available-rooms/', AvailableRoomsView.as_view(), name='get_available_rooms'),
   
   


    path('add-roombooking/', RoomBookingCreateView.as_view(), name='add-roombooking'),
    path('check-overlapping-bookings/',CheckOverlappingBookingsView.as_view(), name='check_overlapping_bookings'),

    path('roombooking-page/<int:id>/',RoomBookingDetailView.as_view(), name='booking-page'), 
    path('booking-list/', RoomBookingListView.as_view(), name='booking-list'),
   
    path('booking-details/<int:booking_id>/', BookingDetailsView.as_view(), name='booking_details'),
    path('my-bookings/<int:user_id>/', UserBookingsView.as_view(), name='my-bookings'),
    path('cancel-booking/<int:booking_id>/', RoomBookingCancellationView.as_view(), name='cancel-booking'),
    path('booking-report/', BookingReportView.as_view(), name='booking-report'),
    path('booking-success/<int:booking_id>/',BookingSuccessAPIView.as_view(), name='booking_success_api'),

    # path('booking-detail/<int:pk>/', RoomBookingDetailView.as_view(), name='booking-list'),

    path('admin/change-booking-status/<int:pk>/',ChangeBookingStatusView.as_view(), name='change-booking-status'),
    path('admin/room-checkout/<int:pk>/', RoomCheckoutView.as_view(), name='room-checkout'),
    
    path('payments/', PaymentListCreateView.as_view(), name='payment-list-create'),
    path('create-razorpay-order/', RazorpayOrderView.as_view(), name='create_razorpay_order'),

    # path('add-reviews/', ReviewListCreateAPIView.as_view(), name='review-list-create'),
    path('add-review/<int:room_id>/<int:user_id>/', AddReviewAPIView.as_view(), name='add_review'),
    path('room-reviews/<int:room_id>/', RoomReviewsListAPIView.as_view(), name='room_reviews_list'),
    path('admin/booking-report/', BookingReportAPIView.as_view(), name='booking-report'),
    path('wallet/<int:user_id>/', WalletDetailView.as_view(), name='wallet-detail'),
]


