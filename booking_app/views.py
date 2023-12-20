from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Category,Room,RoomFeature,RoomBooking,CheckIn,Payment,Review,RoomImage,Wallet
from .serializer import CategorySerializer,RoomSerializer,RoomFeatureSerializer,RoomBookingSerializer,PaymentSerializer,RoomAvailabilityCheckSerializer,ReviewSerializer
from .serializer import DashboardSerializer,RoomImageSerializer,RoomCheckoutSerializer,BookingStatusSerializer,WalletSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView,RetrieveUpdateAPIView,ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.generics import UpdateAPIView
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_list_or_404
import razorpay
from decouple import config
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from datetime import datetime
from django.db.models import Q
from django.utils import timezone
from django.db.models import Count
# # Create your views here.


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 4  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserCategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CustomPageNumberPagination

class CreateCategoryView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
 

    def create(self, request, *args, **kwargs):

        # Access data using names
        category_name = request.POST.get('categoryName', '').strip()
        image = request.FILES.get('image', None)

        # Check if the category name is unique
        if Category.objects.filter(category_name__iexact=category_name).exists():
            return Response({'detail': 'Category with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={'category_name': category_name, 'image': image})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class EditCategoryView(APIView):
    def put(self, request, category_id, *args, **kwargs):
        print(request.data,'dataaaaaaaaaaaaaaaaaaaa')
        updated_category_data = {
            "category_name": request.data.get("category_name"),
          
        }

        img = request.data.get("image")
        if not isinstance(img,str):
            updated_category_data["image"]=img
        try:
            category = Category.objects.get(id=category_id)
            serializer = CategorySerializer(category, data=updated_category_data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# class RoomImageListCreateView(generics.ListCreateAPIView):
#     queryset = RoomImage.objects.all()
#     serializer_class = RoomImageSerializer

# class RoomImageDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = RoomImage.objects.all()
#     serializer_class = RoomImageSerializer
        
        
class BlockUnblockCategoryView(UpdateAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance:
            instance.is_active = not instance.is_active
            instance.save()

            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    



class RoomListView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomListUserView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomDetailsView(APIView):
 

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    def get(self, request, id):
      room = Room.objects.prefetch_related('features').get(id=id)
      serializer = RoomSerializer([room],many = True)
      print(room.cover_image,'oooooooooooooooo')
      return Response(serializer.data,status= status.HTTP_200_OK) 
    def put(self, request, *args, **kwargs):
        room = self.get_object()
        room.is_booked = False
        room.save()
        return Response({'message': 'Checkout successful'}, status=status.HTTP_200_OK)

 
class CreateRoomView(CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class EditRoomView(APIView):
    def put(self, request, room_id, *args, **kwargs):
        try:
            room = Room.objects.get(id=room_id)
            serializer = RoomSerializer(room, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Room.DoesNotExist:
            return Response({"detail": "Room not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

class BlockUnblockRoomView(UpdateAPIView):
    serializer_class = RoomSerializer

    def get_queryset(self):
        return Room.objects.all()

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance:
            instance.is_active = not instance.is_active
            instance.save()

            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Room not found"}, status=status.HTTP_404_NOT_FOUND)


class CreateRoomFeatureView(generics.ListCreateAPIView):
    queryset = RoomFeature.objects.all()
    serializer_class = RoomFeatureSerializer

class RoomFeatureView(generics.ListCreateAPIView):
    queryset = RoomFeature.objects.all()
    serializer_class = RoomFeatureSerializer
   


class BlockUnblockRoomFeatureView(UpdateAPIView):
    queryset = RoomFeature.objects.all()
    serializer_class = RoomFeatureSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'is_blocked' in request.data:
            instance.is_blocked = request.data['is_blocked']
            instance.save()
            return Response(RoomFeatureSerializer(instance).data, status=status.HTTP_200_OK)
        return Response({"error": "is_blocked field not provided in request"}, status=status.HTTP_400_BAD_REQUEST)

       
class EditRoomFeatureView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RoomFeature.objects.all()
    serializer_class = RoomFeatureSerializer


# class RoomAvailabilityCheckView(generics.GenericAPIView):
#     serializer_class = RoomAvailabilityCheckSerializer

#     def get(self, request, *args, **kwargs):
#         check_in_date = self.request.query_params.get('check_in')
#         check_out_date = self.request.query_params.get('check_out')

#         serializer = self.get_serializer(data={'check_in': check_in_date, 'check_out': check_out_date})
#         serializer.is_valid(raise_exception=True)
        
#         # Implement your logic here to check room availability based on check_in_date and check_out_date
#         # For example, query your database to check room availability for the given dates

#         # Assuming is_available is a boolean indicating room availability
#         is_active = True  # Implement your logic to check availability

#         return Response({'is_available': is_active})


class RoomCheckoutView(generics.UpdateAPIView):
    serializer_class = RoomCheckoutSerializer  # Use your RoomCheckout serializer

    def update(self, request, *args, **kwargs):
        room_id = self.kwargs.get('pk')
        room = get_object_or_404(Room, id=room_id)  # Ensure room object exists

        try:
            room.is_active = False  # Update the room's is_active status (change as needed)
            room.save()

            # Optionally, serialize the room details in the response
            serializer = self.get_serializer(room)
            return Response(serializer.data)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# class RoomCheckoutView(generics.UpdateAPIView):
#     queryset = Room.objects.all()  # Define your queryset based on your needs
#     serializer_class = RoomSerializer  # Use your Room serializer

#     def update(self, request, *args, **kwargs):
#         room_id = self.kwargs.get('pk')  # Assuming the room ID is passed as 'pk'
#         try:
#             room = self.get_object()
#             room.is_active = False  # Update the room's is_active status (change as needed)
#             room.save()
            
#             # Optionally, serialize the room details in the response
#             serializer = self.get_serializer(room)
#             print(serializer,"seriallllllllllll")
#             return Response(serializer.data)
#         except Room.DoesNotExist:
#             return Response(status=404)
        

class AvailableRoomsView(APIView):
    serializer_class = RoomSerializer

    def get(self, request):
        check_in_date = request.query_params.get('check_in')
        check_out_date = request.query_params.get('check_out')

        available_rooms = Room.objects.filter(is_active=True)
        serialized_rooms = self.serializer_class(available_rooms, many=True).data
        
        # Manually check room availability for the provided dates and set is_active property
        for room_data in serialized_rooms:
            bookings = room_data['roombookings']
            is_available = all(
                check_in_date >= booking['check_out'] or check_out_date <= booking['check_in']
                for booking in bookings
            )
            room_data['is_active'] = is_available

        return Response(serialized_rooms)

class RoomBookingCreateView(CreateAPIView):
    serializer_class = RoomBookingSerializer
    queryset = RoomBooking.objects.all()

    def create(self, request, *args, **kwargs):
        response = {}
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        check_in = serializer.validated_data['check_in']
        check_out = serializer.validated_data['check_out']
        room = serializer.validated_data['room']  

        # Check for overlapping bookings
        if RoomBooking.objects.filter(room=room, check_out__gt=check_in, check_in__lt=check_out).exists():
            return Response({'message': 'Overlapping booking exists'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        response['data'] = serializer.data
        
        response['response'] = "Room is successfully booked"
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)
    
class CheckOverlappingBookingsView(APIView):
    def post(self, request):
        check_in = request.data.get('check_in')
        check_out = request.data.get('check_out')
        room_id = request.data.get('room')

        # Check for overlapping bookings for the given room and time frame
        overlapping_bookings = RoomBooking.objects.filter(
            Q(room=room_id) &
            (
                (Q(check_in__lt=check_in) & Q(check_out__gt=check_in)) |
                (Q(check_in__lt=check_out) & Q(check_out__gt=check_out)) |
                (Q(check_in__gte=check_in) & Q(check_out__lte=check_out))
            )
        )

        if overlapping_bookings.exists():
            return Response({'message': 'Overlapping booking exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'No overlapping booking'}, status=status.HTTP_200_OK)

    # def post(self, request, *args, **kwargs):
    #     room = get_object_or_404(Room, pk=request.data['room'])
    #     if room.is_active:
    #         return Response({"response": "Room is already booked"}, status=status.HTTP_200_OK)
    #     room.is_active = False
    #     room.save()
    #     checked_in_room = CheckIn.objects.create(
    #         customer=request.user,
    #         room=room,
    #         phone_number=request.data['phone_number'],
    #         email=request.data['email']
    #     )
    #     checked_in_room.save()
    #     return self.create(request, *args, **kwargs)

class RoomBookingListView(generics.ListAPIView):
    queryset = RoomBooking.objects.all()
    serializer_class = RoomBookingSerializer 

    
class RoomBookingDetailView(generics.RetrieveAPIView):
    queryset = RoomBooking.objects.all()
    serializer_class = RoomBookingSerializer

class UserBookingsView(ListAPIView):
    serializer_class = RoomBookingSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return RoomBooking.objects.filter(user_id=user_id)
    

    
class RoomBookingCancellationView(generics.UpdateAPIView):
    queryset = RoomBooking.objects.all()
    serializer_class = RoomBookingSerializer

    def update(self, request, *args, **kwargs):
      try:
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(booking_status='cancelled')  # Update booking status

        # Additional logic after cancellation (if any)...

        return Response({'message': 'Booking cancelled successfully'}, status=status.HTTP_200_OK)
      except RoomBooking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
class RoomCheckoutView(generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'pk'

class BookingReportView(generics.ListAPIView):
    queryset = RoomBooking.objects.all()
    serializer_class = RoomBookingSerializer

    def get_queryset(self):
        # Logic to filter bookings for the report based on parameters, dates, etc.
        # Example: Fetch bookings within a date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            return RoomBooking.objects.filter(check_in__range=[start_date, end_date])
        else:
            return RoomBooking.objects.all()
# class RoomCheckoutView(generics.UpdateAPIView):
#     queryset = RoomBooking.objects.all()
#     serializer_class = RoomBookingSerializer

#     def patch(self, request, *args, **kwargs):
#         booking_id = self.kwargs.get('pk')
#         try:
#             booking = self.get_object()
#             if booking.booking_status == 'completed':
#                 room = booking.room
#                 room.is_active = True  # Set room status to active
#                 room.save()
#                 # Additional logic to update room availability based on the booking
#                 return Response({'message': 'Room status updated successfully'})
#             else:
#                 return Response({'error': 'Booking status is not completed'}, status=status.HTTP_400_BAD_REQUEST)
#         except RoomBooking.DoesNotExist:
#             return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

class RoomBookingPageView(generics.ListAPIView):
    queryset = RoomBooking.objects.all()
    serializer_class = RoomBookingSerializer



class ChangeBookingStatusView(generics.UpdateAPIView):
    queryset = RoomBooking.objects.all()
    serializer_class = RoomBookingSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save(booking_status=request.data.get('booking_status'))

            return Response({'message': 'Booking status updated successfully'}, status=status.HTTP_200_OK)
        except RoomBooking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
# class ChangeBookingStatus(APIView):
#     def put(self, request, booking_id):
#         booking = get_object_or_404(RoomBooking, id=booking_id)
#         new_status = request.data.get('booking_status')

#         # Update the booking status
#         booking.booking_status = new_status
#         booking.save()

#         serializer = RoomBookingSerializer(booking)  # Adjust serializer according to your needs

#         return Response(serializer.data, status=status.HTTP_200_OK)

# class BookingListView(generics.ListAPIView):
#     queryset = Booking.objects.all()
#     serializer_class = BookingSerializer

class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class RazorpayOrderView(APIView):
    
    def post(self, request, *args, **kwargs):
        try:
            booking_id = request.data.get('bookingId')
            amount = request.data.get('amount')

            # Initialize Razorpay client with environment variables
            client = razorpay.Client(auth=(config('RAZORPAY_KEY_ID'), config('RAZORPAY_KEY_SECRET')))
            
            # Create a Razorpay order
            order_params = {
                'amount': float(amount) * 100,  # Amount in paise
                'currency': 'INR',
                'receipt': 'receipt_id',  # Replace with a unique identifier for the order
                'payment_capture': 1,
                'notes': {
                    'booking_id': booking_id,
                    'key': config('RAZORPAY_KEY_ID'),
                }, 
            }

            order = client.order.create(data=order_params)

            return Response(order, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReviewListCreateAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
        
    #     try:
    #         serializer.save()  # Save the validated serializer data
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def perform_create(self, serializer):
    #     serializer.save() # Save the validated serializer data
        

    # def create(self, request, *args, **kwargs):
    #     response = {}
    #     serializer = self.get_serializer(data=request.data)
    #     print(serializer,"hkhkdkjj")
    
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     print(headers,"ddddddddddd")
    #     response['data'] = serializer.data
    #     response['response'] = "Review added"
    #     print(response,"iiiiiiiiiii")
    #     return Response(response, status=status.HTTP_201_CREATED, headers=headers)
    
class ReviewListAPIView(generics.ListAPIView):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class DashboardDataAPIView(APIView):
    def get(self, request):
        # Simulated data for demonstration purposes
        pie_chart_data = [
            {"_id": "Category A", "count": 10},
            {"_id": "Category B", "count": 20},
            # Add more data as needed
        ]

        bar_graph_data = [
            {"_id": "Data 1", "totalTravelers": 5},
            {"_id": "Data 2", "totalTravelers": 15},
            # Add more data as needed
        ]

        statistics_data = {
            "averagePackagePrice": 250,  # Sample statistic values
            "totalAmount": 5000,
            "totalMembers": 50,
            # Add more statistics as needed
        }

        # Constructing the data into the serializer
        serializer_data = {
            'pieChart': pie_chart_data,
            'barGraph': bar_graph_data,
            'statistics': statistics_data,
        }

        serializer = DashboardSerializer(data=serializer_data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class BookingReportView(generics.ListAPIView):
    serializer_class = RoomBookingSerializer

    def get_queryset(self):
        year = int(self.kwargs.get('year'))
        month = int(self.kwargs.get('month'))
        
        start_date = datetime(year, month, 1)
        next_month = month + 1 if month < 12 else 1
        next_year = year + 1 if month == 12 else year
        end_date = datetime(next_year, next_month, 1)

        return RoomBooking.objects.filter(booking_date__gte=start_date, booking_date__lt=end_date).values('booking_date').annotate(count=Count('id')).order_by('booking_date')
    
class WalletDetailView(generics.RetrieveAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer