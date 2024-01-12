from accounts.serializers import UserSerializer
from .models import Category,Room,RoomFeature,RoomBooking,CheckIn,Payment,Review,RoomImage,Wallet
from accounts.models import AccountUser
from rest_framework import serializers
from django.db.models import Count


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class RoomFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomFeature
        fields =  '__all__'

class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = '__all__'

class RoomListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required= False)
    features = RoomFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = '__all__'
        
class RoomSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(read_only=True)
    # features = RoomFeatureSerializer(many=True,read_only=True)

    class Meta:
        model = Room
        fields = ['title','category','price_per_night','capacity','room_size','cover_image','features','description','created_at','updated_at','is_active']

    # def create(self, validated_data):
    #     print(validated_data,"validste")
    #     category_data = validated_data.pop('category')
    #     features_data = validated_data.pop('features')

    #     # Create or get Category
    #     category_instance = Category.objects.get(**category_data)

    #     # Create Room instance with the retrieved or created Category
    #     room = Room.objects.create(category=category_instance, **validated_data)

    #     # Create or get RoomFeature instances and add them to the Room
    #     # features_instances= [RoomFeature.objects.get(**feature_data)[0] for feature_data in features_data]
    #     room.features.add(*features_instances)

    #     return room

class RoomDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    features = RoomFeatureSerializer(many=True,read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'title', 'category', 'price_per_night', 'capacity', 'room_size', 'cover_image', 'features', 'description', 'created_at', 'updated_at', 'is_active']

class SingleRoomDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    features = RoomFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'title', 'category', 'price_per_night', 'capacity', 'room_size', 'cover_image', 'features', 'description', 'created_at', 'updated_at', 'is_active']

class RoomBookingSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()  # Serializer method field for user email
    room_title = serializers.SerializerMethodField() 
    # total_amount = serializers.SerializerMethodField()  

    # Serializer method field for room title

    class Meta:
        model = RoomBooking
        fields = '__all__'

    def get_user_email(self, obj):
        print(obj,"kkkk")
        print(obj.number_of_guests,"room")
        user=obj.user
        
        return user.email if user.email else None  # Access user email
    
    def get_room_title(self, obj):
        room=obj.room
        return room.title if room.title else None  # Access room title
    
    def get_price(self, obj):
        # Replace 'price_field_name' with the actual field name from your Room model
        room=obj.room
        return room.price_per_night if room else None

    def validate(self, data):
        # Ensure check_out is not before check_in
        check_in = data.get('check_in')
        check_out = data.get('check_out')
        if check_in and check_out and check_out < check_in:
            raise serializers.ValidationError("Check-out date cannot be before check-in date.")
        return data
    
class RoomBookingSerializer1(serializers.Serializer):
       class Meta:
        model = RoomBooking
        fields = '__all__'
    
class RoomAvailabilityCheckSerializer(serializers.Serializer):
    check_in = serializers.DateField()
    check_out = serializers.DateField()
    # Other fields if needed

    def validate(self, data):
        """
        Validate check-in and check-out dates.
        Ensure check_out is not before check_in.
        """
        check_in = data.get('check_in')
        check_out = data.get('check_out')

        if check_in and check_out and check_out < check_in:
            raise serializers.ValidationError("Check-out date cannot be before check-in date.")

        # Additional validation if required
        
        return data
    
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'   


class CheckinSerializer(serializers.ModelSerializer):
    room_id = serializers.IntegerField(source='room.pk')
  
    customer_id = serializers.IntegerField(source='customer.pk')
    customer_name = serializers.CharField(source='customer.username')

    class Meta:
        model = CheckIn
        fields = ('phone_number', 'email', 'customer_id', 'customer_name', 'room_id')

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('room', 'user', 'rating', 'comment', 'created_at')
        unique_together = ['room', 'user']
class BookingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomBooking
        fields = ['booking_status']
class RoomCheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [ 'is_active']

class DashboardSerializer(serializers.Serializer):
    pieChart = serializers.ListField(child=serializers.DictField())
    barGraph = serializers.ListField(child=serializers.DictField())
    statistics = serializers.DictField()    

    def get_pieChart(self, obj):
        # Retrieve and format pie chart data
        # Example:
        pie_chart_data = RoomBooking.objects.values('room__title').annotate(count=Count('id'))
        return pie_chart_data

    def get_barGraph(self, obj):
      
        bar_graph_data = RoomBooking.objects.values('room__title').annotate(totalBookings=Count('id'))
        return bar_graph_data

    def get_roomIndication(self, obj):
      
        room_indication_data = Room.objects.values('id', 'title')
        return room_indication_data
    

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('user', 'balance')