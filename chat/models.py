#models.py


from django.db import models
from accounts.models import AccountUser


class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True,default="")
    provider= models.ForeignKey(AccountUser, on_delete=models.CASCADE, related_name='provider_room',default="")
    username= models.CharField(max_length=255,default="")

    def __str__(self):
        return self.name

class ChatMessage(models.Model):
    user = models.ForeignKey(AccountUser, on_delete=models.CASCADE, related_name='sent_messages',default="")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} to {self.room.name}"



























# from django.db import models
# from accounts.models import AccountUser


# class ChatRoom(models.Model):
#     name = models.CharField(max_length=255, unique=True)
#     provider= models.ForeignKey(AccountUser, on_delete=models.CASCADE, related_name='provider_room')
#     username= models.CharField(max_length=255)

#     def __str__(self):
#         return self.name

# class Message(models.Model):
#     user = models.ForeignKey(AccountUser, on_delete=models.CASCADE, related_name='sent_messages')
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
#     is_seen = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.user.first_name} to {self.chatroom.name}"


















































# from django.db import models
# from accounts.models import AccountUser

# class Chat(models.Model):
#     users = models.ManyToManyField(AccountUser, related_name='user_chats')
#     admin = models.ManyToManyField(AccountUser, related_name='admin_chat')

# class Message(models.Model):
#     chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
#     sender = models.ForeignKey(AccountUser, related_name='sent_messages', on_delete=models.CASCADE)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)





















# from django.db import models
# from shortuuid import ShortUUID
# from accounts.models import AccountUser

# class ChatRoom(models.Model):
# 	roomId = ShortUUID()
# 	type = models.CharField(max_length=10, default='DM')
# 	member = models.ManyToManyField(AccountUser)
# 	name = models.CharField(max_length=20, null=True, blank=True)

# 	def __str__(self):
# 		return self.roomId + ' -> ' + str(self.name)

# class ChatMessage(models.Model):
# 	chat = models.ForeignKey(ChatRoom, on_delete=models.SET_NULL, null=True)
# 	user = models.ForeignKey(AccountUser, on_delete=models.SET_NULL, null=True)
# 	message = models.CharField(max_length=255,default='')
# 	timestamp = models.DateTimeField(auto_now_add=True)

# 	def __str__(self):
# 		return self.message














# from django.db import models
# from accounts.models import AccountUser

# class ChatMessage(models.Model):
#     sender = models.ForeignKey(AccountUser, related_name='sent_messages', on_delete=models.CASCADE)
#     recipient = models.ForeignKey(AccountUser, related_name='received_messages', on_delete=models.CASCADE)
#     text = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.sender} to {self.recipient}: {self.text}"




























# # chat/models.py
# from django.db import models
# from accounts.models import AccountUser

# class ChatMessage(models.Model):
#     sender = models.ForeignKey(AccountUser, on_delete=models.CASCADE, related_name='sent_messages')
#     receiver = models.ForeignKey(AccountUser, on_delete=models.CASCADE, related_name='received_messages')
#     message = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     sendername = models.TextField(max_length=100, null=True,blank=True)
    
#     def __str__(self):
#         return f'{self.sender} to {self.receiver}: {self.message}'


















# from django.db import models
# from accounts.models import AccountUser

# class ChatMessage(models.Model):
#     sender = models.ForeignKey(AccountUser, on_delete=models.CASCADE, related_name='sent_messages')
#     receiver = models.ForeignKey(AccountUser, on_delete=models.CASCADE, related_name='received_messages')
#     message = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
    














# from django.db import models

# from accounts.models import AccountUser



# class ChatRoom(models.Model):
#     members = models.ManyToManyField(AccountUser, related_name='chat_rooms')

#     def __str__(self):
#         return ', '.join([str(member) for member in self.members.all()])

# class Message(models.Model):
#     room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
#     sender = models.ForeignKey(AccountUser, on_delete=models.CASCADE)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     is_seen = models.BooleanField(default=False)

#     class Meta:
#         ordering = ('timestamp',)

#     def __str__(self):















# from django.db import models

# from accounts.models import AccountUser


# class ChatMessage(models.Model):
#     sender = models.ForeignKey(AccountUser, on_delete=models.CASCADE, related_name='sent_messages')
#     receiver = models.ForeignKey(AccountUser, on_delete=models.CASCADE, related_name='received_messages')
#     message = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     sendername = models.TextField(max_length=100, null=True,blank=True)
    
#     def __str__(self):
#         return f'{self.sender} to {self.receiver}: {self.message}'


# class ChatRoom(models.Model):
#     WAITING = 'waiting'
#     ACTIVE = 'active'
#     CLOSED = 'closed'

#     CHOICES_STATUS = (
#         (WAITING, 'Waiting'),
#         (ACTIVE, 'Active'),
#         (CLOSED, 'Closed'),
#     )

#     uuid = models.CharField(max_length=255)
#     client = models.CharField(max_length=255)
#     agent = models.ForeignKey(AccountUser, related_name='rooms', blank=True, null=True, on_delete=models.SET_NULL)
#     messages = models.ManyToManyField(Message, blank=True)
#     url = models.CharField(max_length=255, blank=True, null=True)
#     status = models.CharField(max_length=20, choices=CHOICES_STATUS, default=WAITING)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
    #     ordering = ('-created_at',)
    
    # def __str__(self):
    #     return f'{self.client} - {self.uuid}'
