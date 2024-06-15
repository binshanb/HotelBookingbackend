from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Category,Room,RoomFeature,RoomBooking,CheckIn,Payment,Review,RoomImage,Wallet
from accounts.models import AccountUser
from .serializer import CategorySerializer,RoomSerializer,WalletSerializer,RoomFeatureSerializer,RoomBookingSerializer,PaymentSerializer,RoomListSerializer,RoomAvailabilityCheckSerializer,ReviewSerializer,RoomDetailSerializer,RoomCheckoutSerializer,SingleRoomDetailSerializer,DashboardSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView,RetrieveUpdateAPIView,ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.generics import UpdateAPIView
from django.utils import timezone
import pytz

from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_list_or_404
import os
from django.http import Http404
import razorpay
from decouple import config
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from datetime import datetime
from django.db.models import Q
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from django.db.models import Sum

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
        category_name = request.POST.get('category_name', '').strip()
        image = request.FILES.get('image', None)

        # Check if the category name is unique
        if Category.objects.filter(category_name__iexact=category_name).exists():
            return Response({'detail': 'Category with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        data = {
            'category_name': category_name,
            'image': image
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
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
    serializer_class = RoomListSerializer

class RoomRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomListUserView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomDetailSerializer


class RoomDetailsView(APIView):
    queryset = Room.objects.all()
    serializer_class = SingleRoomDetailSerializer


    def get(self, request, id):
      room = Room.objects.prefetch_related('features').get(id=id)
      serializer = SingleRoomDetailSerializer([room],many = True)
      print(room.cover_image,'oooooooooooooooo')
      return Response(serializer.data,status= status.HTTP_200_OK) 
    
    def put(self, request, *args, **kwargs):
        room = self.get_object()
        room.is_booked = False
        room.save()
        return Response({'message': 'Checkout successful'}, status=status.HTTP_200_OK)

 
# class CreateRoomView(CreateAPIView):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
        
#         # Retrieve the room instance created by the serializer
#         room_instance = serializer.instance

#         # Customize the response data to include category and features
#         response_data = serializer.data
#         response_data['category'] = room_instance.category.id  # Adjust to your model structure
#         response_data['features'] = [feature.id for feature in room_instance.features.all()]  # Adjust to your model structure
        
#         return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

class CreateRoomView(APIView):
    def post(self, request, format=None):
        print(request.data,"datataa")
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class EditRoomView(APIView):
    def put(self, request, room_id, *args, **kwargs):
        try:
            room = Room.objects.get(id=room_id)
            serializer = RoomSerializer(room, data=request.data, partial=True)
            print(serializer,"serialllll")

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
    serializer_class = RoomFeatureSerializer

    def get_queryset(self):
        return RoomFeature.objects.all()

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance:
            instance.is_active = not instance.is_active
            instance.save()

            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Feature not found"}, status=status.HTTP_404_NOT_FOUND)

       
class EditRoomFeatureView(UpdateAPIView):
    
    queryset = RoomFeature.objects.all()
    serializer_class = RoomFeatureSerializer
   
    lookup_field ="id"


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
        diff = self.request.data.get('diffDays')
        number_of_guests = self.request.data.get('number_of_guests')
        data=request.data
        print(data,"request.data")
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        check_in = serializer.validated_data['check_in']
        check_out = serializer.validated_data['check_out']
        room = serializer.validated_data['room']  
        
        price_per_night = room.price_per_night
      
        total_amount = diff * int(number_of_guests )* price_per_night

        check_in = check_in.replace(hour=12, minute=0, second=0, microsecond=0)
        check_out = check_out.replace(hour=12, minute=0, second=0, microsecond=0)

            # If the check_out is inclusive, add a day to it to make it 12:00 PM the next day
        check_out += timedelta(days=1)

# Convert the datetime objects to UTC
        aware_check_in = timezone.localtime(check_in, timezone.utc)
        aware_check_out = timezone.localtime(check_out, timezone.utc)
        # Convert check-in and check-out dates to UTC before comparing or storing
        # local_check_in = timezone.localtime(aware_check_in)
        # local_check_out = timezone.localtime(aware_check_out) 
        # Check for overlapping bookings
       
        
 
        if RoomBooking.objects.filter(room=room, check_out__gt=aware_check_in, check_in__lt=aware_check_out).exists():
            return Response({'message': 'Overlapping booking exists'}, status=status.HTTP_400_BAD_REQUEST)
        
       
    
        

        self.perform_create(serializer)

        instance = serializer.instance
        instance.total_amount = total_amount
        instance.save()
        serialized_data = serializer.data
        
        headers = self.get_success_headers(serialized_data)


        response['data'] = serialized_data
        
        response['response'] = "Room is successfully booked"
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)
    

        


class BookingDetailsView(APIView):
    def get(self, request, booking_id):
        try:
            # Retrieve RoomBooking object based on booking_id
            room_booking = RoomBooking.objects.get(id=booking_id)

            # Calculate the number of days between check-in and check-out dates
            num_of_days = (room_booking.check_out - room_booking.check_in).days

            # Calculate the price per day
            price_per_day = room_booking.room.price_per_night
            num_of_guests = room_booking.number_of_guests
            # Get total amount from the RoomBooking object
            total_amount = room_booking.total_amount

            # Prepare data to return
            data = {
                'booking_id': room_booking.id,
                'num_of_days': num_of_days,
                'price_per_day': price_per_day,
                'num_of_guests': num_of_guests,
                'total_amount': total_amount
                # Add other fields if needed
            }

            return Response(data, status=status.HTTP_200_OK)

        except RoomBooking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

    
class CheckOverlappingBookingsView(APIView):
    def post(self, request):
        print(request.data,"datassssssssssss")
        check_in = request.data.get('check_in')
        check_out = request.data.get('check_out')
        room_id = request.data.get('room')
        
        check_in_datetime = datetime.strptime(check_in[:-1], '%Y-%m-%dT%H:%M:%S.%f')
        check_out_datetime = datetime.strptime(check_out[:-1], '%Y-%m-%dT%H:%M:%S.%f')

                # Define UTC timezone
        utc = pytz.UTC

        # Convert datetime objects to UTC timezone
        check_in_datetime = utc.localize(check_in_datetime)
        check_out_datetime = utc.localize(check_out_datetime)
        # Check for overlapping bookings for the given room and time frame
        overlapping_bookings = RoomBooking.objects.filter(
            Q(room=room_id) &
            (
                (Q(check_in__lt=check_in_datetime) & Q(check_out__gt=check_in_datetime)) |
                (Q(check_in__lt=check_out_datetime) & Q(check_out__gt=check_out_datetime)) |
                (Q(check_in__gte=check_in_datetime) & Q(check_out__lte=check_out_datetime))
            )
        )

        if overlapping_bookings.exists():
            return Response({'message': 'Overlapping booking exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'No overlapping booking'}, status=status.HTTP_200_OK)



class RoomBookingListView(generics.ListAPIView):
    queryset = RoomBooking.objects.all()
    serializer_class = RoomBookingSerializer 

    
class RoomBookingDetailView(generics.RetrieveAPIView):
    queryset = RoomBooking.objects.all()
    serializer_class = RoomBookingSerializer
    def get_object(self):
        booking_id = self.kwargs['id']
        print(RoomBooking.objects.get(id=booking_id).total_amount,"kkkkooliku")
        return RoomBooking.objects.get(id=booking_id)

   
    


class BookingSuccessAPIView(APIView):
    def get(self, request, booking_id):
        try:
            # Assuming you have a Booking model with fields like booking_id and price
            # Retrieve the booking details from the database using the provided booking_id
            booking = RoomBooking.objects.get(id=booking_id)

            # Construct a response with booking details and additional information
            response_data = {
                "booking_id": booking.id,
                
                # Include other relevant details from the booking model
            }

            return Response(response_data)
        
        except RoomBooking.DoesNotExist:
            return Response({"error": "Booking does not exist"}, status=404)
        
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class UserBookingsView(ListAPIView):
    serializer_class = RoomBookingSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return RoomBooking.objects.filter(user_id=user_id)
    

    

class RoomBookingCancellationView(APIView):
    def post(self, request, booking_id):
        cancellation_reason = request.data.get('cancellation_reason')
        user_id = request.data.get('user')
        user=AccountUser.objects.get(id=user_id)
        
        try:
            booking = get_object_or_404(RoomBooking, pk=booking_id, user=user)
            booking.booking_status = 'cancelled'
            booking.cancellation_reason = cancellation_reason
            booking.save()

            # Refund the amount to the user's wallet
            user_wallet, _ = Wallet.objects.get_or_create(user=user)
            refund_amount = booking.total_amount  # Replace this with your booking amount field
            user_wallet.balance += refund_amount
            user_wallet.save()
            print(user_wallet.balance,"balance")

            return Response({'message': 'Booking cancelled successfully and amount refunded to wallet'}, status=status.HTTP_200_OK)
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
   
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            return RoomBooking.objects.filter(check_in__range=[start_date, end_date])
        else:
            return RoomBooking.objects.all()

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


class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class RazorpayOrderView(APIView):
    
    def post(self, request, *args, **kwargs):
        try:
            booking_id = request.data.get('bookingId')
            amount = request.data.get('amount')

            # Initialize Razorpay client with environment variables
            client = razorpay.Client(auth=(os.environ.get('RAZORPAY_KEY_ID'), os.environ.get('RAZORPAY_KEY_SECRET')))
            
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



class AddReviewAPIView(APIView):
    def post(self, request, room_id, user_id):
        try:
            room = get_object_or_404(Room, pk=room_id)
            user = get_object_or_404(AccountUser, pk=user_id)

            existing_review = Review.objects.filter(room=room, user=user).first()

            if existing_review:
                # If a review exists for this room and user, update it
                serializer = ReviewSerializer(existing_review, data=request.data)
            else:
                # If no review exists, create a new one
                review_data = {
                    'room': room.id,
                    'user': user.id,
                    'rating': request.data.get('rating'),
                    'comment': request.data.get('comment')
                }
                serializer = ReviewSerializer(data=review_data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Room.DoesNotExist:
            return Response({'error': 'Room does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except AccountUser.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






# View to get a list of reviews for a specified room
class RoomReviewsListAPIView(APIView):
    def get(self, request, room_id):
        print(request,"reqqqqqqqqqqq")
        try:
            room_reviews = Review.objects.filter(room=room_id)
            serializer = ReviewSerializer(room_reviews, many=True)
            print(serializer,"serisllllll")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Review.DoesNotExist:
            return Response({'error': 'Room reviews not found'}, status=status.HTTP_404_NOT_FOUND)



class DashboardDataAPIView(APIView):
     def get(self, request):
        pie_chart_data = RoomBooking.objects.values ('room__category__category_name', 
            'room__category__id',
    
        ).annotate(count=Count('id'))

        # Calculate bar graph data dynamically
        bar_graph_data = RoomBooking.objects.values( 'room__title', 
            'room__id',  # Include room ID
        ).annotate(totalBookings=Count('id'))

        # Calculate statistics data dynamically
        statistics_data = {
            "AverageRoomBookingPrice": RoomBooking.objects.aggregate(avg_price=Sum('room__price_per_night'))['avg_price'] or 0,
            "TotalBookingAmount": RoomBooking.objects.aggregate(total_amounts=Sum('total_amount'))['total_amounts'] or 0,
            "TotalBookings": RoomBooking.objects.count(),
        }

        room_indication = {}
        for room_booking in RoomBooking.objects.all():
            room_id = room_booking.room.id
            category_name = room_booking.room.category.category_name
            # Assign indication details to room ID or category name
            room_indication[room_id] = {'category_name': category_name, 'indication': 'some_color'}
        # Constructing the data into the serializer
        serializer_data = {
            'pieChart': pie_chart_data,
            'barGraph': bar_graph_data,
            'statistics': statistics_data,
        }

        serializer = DashboardSerializer(data=serializer_data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class BookingReportAPIView(APIView):
    def get(self, request):
        # Get total booking counts and total amount based on room category
        category_data = RoomBooking.objects.values('room__category__category_name') \
            .annotate(booking_count=Count('id'), total_amount=Sum('total_amount'))

        # Construct the response data
        response_data = {
            'categoryData': category_data,
            # Add other data as needed
        }

        return Response(response_data, status=status.HTTP_200_OK)

    
class WalletDetailView(APIView):
    def get(self, request, user_id):
        print("enterde into wallet function")
        wallet = get_object_or_404(Wallet, user_id=user_id)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)
