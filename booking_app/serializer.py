from accounts.serializers import UserSerializer
from .models import Category,Room,RoomFeature,RoomBooking,CheckIn,Payment,Review,RoomImage,Wallet
from accounts.models import AccountUser
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class RoomFeatureSerializer(serializers.ModelSerializer):
    print("serialllllll")
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
    category = CategorySerializer()
    features = RoomFeatureSerializer(many=True)

    class Meta:
        model = Room
        fields = '__all__'

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        features_data = validated_data.pop('features')
        
        category, _ = Category.objects.get_or_create(**category_data)
        room = Room.objects.create(category=category, **validated_data)
        for feature_data in features_data:
            feature, _ = RoomFeature.objects.get_or_create(**feature_data)
            room.features.add(feature)

        return room




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
    room_slug = serializers.SlugField(source='room.room_slug')
    customer_id = serializers.IntegerField(source='customer.pk')
    customer_name = serializers.CharField(source='customer.username')

    class Meta:
        model = CheckIn
        fields = ('phone_number', 'email', 'customer_id', 'customer_name', 'room_id', 'room_slug',)

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

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('user', 'balance')