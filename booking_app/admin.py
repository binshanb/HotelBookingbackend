from django.contrib import admin
from .models import Room, Category, Customer, Payment, CheckIn, CheckOut,RoomFeature,RoomBooking,RoomImage,Review

# Register your models here.


admin.site.register(Room)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Payment)
admin.site.register(CheckIn)
admin.site.register(CheckOut)
admin.site.register(RoomBooking)
admin.site.register(RoomImage)
admin.site.register(Review)


admin.site.register(RoomFeature)