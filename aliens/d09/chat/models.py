from django.contrib.auth.models import User
from django.db import models


class ChatRoom(models.Model):
    name = models.CharField(max_length=64, unique=True, null=False)


class Message(models.Model):
    body = models.TextField('body')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='to_user')
    timestamp = models.DateTimeField('timestamp', auto_now_add=True, editable=False)

    def __str__(self):
        return str(self.id)


class ChatRoomUser(models.Model):

    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
