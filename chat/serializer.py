# serializers.py

from rest_framework import serializers
from .models import ChatMessage, ChatRoom

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields ='__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'user', 'content', 'timestamp','is_seen']

    # # You can include serializers for the sender and receiver fields if needed
    # sender = serializers.StringRelatedField()
    # receiver = serializers.StringRelatedField()

class UnseenMessagesCountSerializer(serializers.Serializer):
    unseen_count = serializers.IntegerField()

class MessageCountSerializer(serializers.Serializer):
    provider_id = serializers.IntegerField()
    total_message_count = serializers.IntegerField()























# # serializers.py

# from rest_framework import serializers
# from .models import Message, ChatRoom

# class ChatRoomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ChatRoom
#         fields ='__all__'

# class MessageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Message
#         fields = ['id', 'user', 'content', 'timestamp','is_seen']

 

# class UnseenMessagesCountSerializer(serializers.Serializer):
#     unseen_count = serializers.IntegerField()

# class MessageCountSerializer(serializers.Serializer):
#     _id = serializers.IntegerField()
#     total_message_count = serializers.IntegerField()












































# from rest_framework import serializers
# from .models import ChatRoom, ChatMessage
# from accounts.serializers import UserSerializer

# class ChatRoomSerializer(serializers.ModelSerializer):
# 	member = UserSerializer(many=True, read_only=True)
# 	members = serializers.ListField(write_only=True)

# 	def create(self, validatedData):
# 		memberObject = validatedData.pop('members')
# 		chatRoom = ChatRoom.objects.create(**validatedData)
# 		chatRoom.member.set(memberObject)
# 		return chatRoom

# 	class Meta:
# 		model = ChatRoom
# 		exclude = ['id']

# class ChatMessageSerializer(serializers.ModelSerializer):
# 	userName = serializers.SerializerMethodField()
# 	userImage = serializers.ImageField(source='user.image')

# 	class Meta:
# 		model = ChatMessage
# 		exclude = ['id', 'chat']

# 	def get_userName(self, Obj):
# 		return Obj.user.first_name + ' ' + Obj.user.last_name

















# from rest_framework import serializers
# from .models import ChatMessage

# class ChatMessageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ChatMessage
#         fields = '__all__'












# from rest_framework import serializers
# from chat.models import ChatRoom, Message
# from django.utils.timesince import timesince

# from accounts.models import AccountUser



# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AccountUser
#         fields = ['id', 'email', 'first_name', 'last_name','username', 'profile_pic']


# class ChatRoomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ChatRoom
#         fields = '__all__'


# class MessageSerializer(serializers.ModelSerializer):
#     sender_email = serializers.EmailField(source='sender.email', read_only=True)
#     sender_profile_pic = serializers.SerializerMethodField(read_only=True)
#     created = serializers.SerializerMethodField(read_only=True)
    
#     class Meta:
#         model = Message
#         fields = '__all__'
    
#     def get_sender_profile_pic(self, obj):
#         return obj.sender.profile_pic.url if obj.sender.profile_pic else None

#     def get_created(self, obj):
#         return timesince(obj.timestamp)

    




# class ChatRoomListSerializer(serializers.ModelSerializer):
#     unseen_message_count = serializers.SerializerMethodField()
#     members = UserSerializer(many=True)

#     class Meta:
#         model = ChatRoom
#         fields = '__all__'

#     def get_unseen_message_count(self, obj):
#         user = self.context['request'].user
#         return Message.objects.filter(room=obj, is_seen=False).exclude(sender=user).count()

#     def to_representation(self, instance):
#         user = self.context['request'].user
#         members = instance.members.exclude(id=user.id)
#         data = super(ChatRoomListSerializer, self).to_representation(instance)
#         data['members'] = UserSerializer(members, many=True).data
#         return data




















# from rest_framework import serializers
# from .models import ChatMessage
# # from accounts.serializers import UserSerializer  # Import the AccountUser serializer if available





# class ChatMessageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ChatMessage
#         fields = '__all__'
























# from rest_framework import serializers
# from .models import Message

# class MessageSerializer(serializers.ModelSerializer):
#        class Meta:
#            model = Message
#            fields = ('id', 'username', 'content', 'timestamp')
#            read_only_fields = ('id', 'timestamp')








           
# class ChatRoomListSerializer(serializers.ModelSerializer):
#     unseen_message_count = serializers.SerializerMethodField()
#     members = UserSerializer(many=True)

#     class Meta:
#         model = ChatRoom
#         fields = '__all__'

# # for notifications
#     def get_unseen_message_count(self, obj):
#         user = self.context['request'].user
#         return Message.objects.filter(room=obj, seen=False).exclude(sender=user).count()

#     def to_representation(self, instance):
#         user = self.context['request'].user
#         members = instance.members.exclude(id=user.id)
#         data = super(ChatRoomListSerializer, self).to_representation(instance)
#         data['members'] = UserSerializer(members, many=True).data
#         return data