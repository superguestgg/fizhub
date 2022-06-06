from django.db import models
class Room(models.Model):
    room_name = models.CharField(max_length=100, default="no name")
    room_theme = models.CharField(max_length=50, default="No theme")
    room_description = models.CharField(max_length=1000, default="no description")
    room_rights = models.IntegerField(default=0)
    room_type_channel = models.BooleanField(default=False)
    room_channel_admin_password = models.CharField(max_length=50, default="12345")
    room_type_private = models.BooleanField(default=False)
    room_type_password = models.BooleanField(default=False)
    room_type_token = models.BooleanField(default=False)
    room_password = models.CharField(max_length=50, default="no password")
    room_messages_count = models.IntegerField(default=0)
    def __str__(self):
        return str(self.room_name)+" ______ description: "+str(self.room_description)
class Message(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    answer_for = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    message_text = models.CharField(max_length=2000, default="empty message")
    is_pinned = models.BooleanField(default=False)
    answers_count = models.IntegerField(default=0)
    def __str__(self):
        return str(self.message_text)+" ______ room: "+str(self.room_id.room_name)
"""class Group(models.Model):
    group_id=models.IntegerField()
    group_rooms=models."""