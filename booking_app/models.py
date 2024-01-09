from django.db import models
from accounts.models import AccountUser
from django.core.validators import MinValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
import pytz

# Create your models here.



class RoomFeature(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Room(models.Model):
    title = models.CharField(max_length=30)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price_per_night = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    room_slug = models.SlugField()
    capacity =  models.PositiveIntegerField(validators=[MinValueValidator(0)])
    room_size = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    cover_image = models.ImageField(upload_to='media/media/images')
    features = models.ManyToManyField(RoomFeature)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class RoomImage(models.Model):
    room = models.ForeignKey(Room, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/room_images')

    def __str__(self):
        return f"Image for {self.room.title}"

class Category(models.Model):
    category_name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='media/images',default='path/to/default_image.jpg' )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


    def __str__(self):
        return self.category_name



class Customer(models.Model):

    customer = models.ForeignKey(AccountUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.customer




class RoomBooking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='roombookings')
    user = models.ForeignKey(AccountUser, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    
    number_of_guests = models.IntegerField(null=True, blank=True)
    total_amount = models.IntegerField(default=0)
    
    booking_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    ], default='pending')
    booking_notes = models.TextField(blank=True)
    booking_date = models.DateTimeField(default=timezone.now) 

    def clean(self):
        # Ensure check_out is not before check_in
        if self.check_in and self.check_out and self.check_out < self.check_in:
            raise ValidationError("Check-out date cannot be before check-in date.")
        
    
    def __str__(self):

        formatted_check_in = self.check_in.strftime("%Y-%m-%d %I:%M %p")
        formatted_check_out = self.check_out.strftime("%Y-%m-%d %I:%M %p")

        return f"{self.user.email} - Check-in (UTC): {formatted_check_in}, Check-out (UTC): {formatted_check_out}"

        # ist = pytz.timezone('Asia/Kolkata')
        
        # # Convert check-in and check-out times to IST timezone
        # ist_check_in = self.check_in.astimezone(ist)
        # ist_check_out = self.check_out.astimezone(ist)

        # formatted_check_in = ist_check_in.strftime("%Y-%m-%d %I:%M %p")
        # formatted_check_out = ist_check_out.strftime("%Y-%m-%d %I:%M %p")

        # Calculate the duration in hours between check-in and check-out
        # duration_hours = (ist_check_out - ist_check_in).total_seconds() / 3600

        # return f"{self.user.email} - Check-in (IST): {formatted_check_in}, Check-out (IST): {formatted_check_out}, Duration: {duration_hours} hours"

class Payment(models.Model):
    PAYMENT_RAZORPAY = 'razorpay'
    payment_choices = [
        (PAYMENT_RAZORPAY, 'Razorpay'),
    ]

    customer = models.ForeignKey(AccountUser, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100, default='some_default_value')
    payment_method = models.CharField(max_length=100, choices=payment_choices, default=PAYMENT_RAZORPAY)
    amount_paid = models.CharField(max_length=100,default='0')
    status = models.CharField(max_length=100, default='some_default_value')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.customer.email} -- {self.payment_method}"

class CheckIn(models.Model):
    customer = models.ForeignKey(AccountUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=14, null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.room.room_slug


class CheckOut(models.Model):
    customer = models.ForeignKey(AccountUser, on_delete=models.CASCADE)
    check_out_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.email




class Review(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(AccountUser, on_delete=models.CASCADE)

    rating = models.PositiveIntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('room', 'user')

class Wallet(models.Model):
    user = models.OneToOneField(AccountUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.user.email