from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
from django.dispatch import receiver


#<---------Basics Credentials-------------->

class AccountUserManager(BaseUserManager):  # account user manager
    def create_user(self,email,password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
    
        user = self.model(
            email= self.normalize_email(email),
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email, password=None):
        user = self.create_user(
            email=self.normalize_email(email), password=password,)
        user.is_admin = True 
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Role(models.TextChoices):
    GUEST = 'guest','Guest'
    ADMIN = 'admin','Admin'

class AccountUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    image = models.ImageField(upload_to="media/images", null=True,blank=True, default="profile-img.jpg")
    role = models.CharField(max_length=20, choices=Role.choices, default='')

     # Additional fields
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    otp = models.CharField(max_length=6, null=True, blank=True)  # Adding OTP field

    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    objects = AccountUserManager()

    def __str__(self):
        return self.email


    
    def has_perm(self, perm, obj = None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True



#<---------------------------Basics Credentials-----End------------------>


# class Profile(models.Model):
#     user = models.OneToOneField(AccountUser, on_delete=models.CASCADE)
#     full_name = models.CharField(max_length=1000)
#     bio = models.CharField(max_length=100)
#     image = models.ImageField(upload_to="user_images", default="default.jpg")
#     verified = models.BooleanField(default=False)

#     def save(self, *args, **kwargs):
#         if self.full_name == "" or self.full_name == None:
#             self.full_name = self.user.username
#         super(Profile, self).save(*args, **kwargs)


# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

# post_save.connect(create_user_profile, sender=AccountUser)
# post_save.connect(save_user_profile, sender=AccountUser) 

# class ChatMessage(models.Model):
#     user = models.ForeignKey(AccountUser,on_delete=models.CASCADE,related_name="user")
#     sender = models.ForeignKey(AccountUser,on_delete=models.CASCADE,related_name="sender")
#     receiver = models.ForeignKey(AccountUser,on_delete=models.CASCADE,related_name="receiver")
    
#     message = models.CharField(max_length=1000)
#     is_read = models.BooleanField(default=False)
#     date = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['date']
#         verbose_name_plural = "Message"
    
#     def __str__(self):
#         return f"{self.sender} - {self.receiver}"
    

#     @property
#     def sender_profile(self):
#         sender_profile= AccountUser.objects.get(user=self.sender)
#         return sender_profile
    
#     @property
#     def receiver_profile(self):
#         receiver_profile= AccountUser.objects.get(user=self.receiver)
#         return receiver_profile