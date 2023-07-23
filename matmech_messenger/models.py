from django.db import models


class Guest(models.Model):
    name = models.CharField(max_length=100, default="no name")
    hashed_password = models.IntegerField(default=0)
    about = models.TextField(max_length=5000, default="no information")
    pub_date = models.DateTimeField('date created')
    icon = models.URLField()

    def __str__(self):
        return f"{self.name} ______ about: {self.about}"


class GuestSession(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=100, default="its impossible")
    http_user_agent = models.TextField(max_length=500, default='its impossible')

    def __str__(self):
        return str(self.guest.name) + " key: " + str(self.session_key)


class PrivateChat(models.Model):
    authors = models.ManyToManyField(Guest)
    author_0_not_checked_messages_count = models.IntegerField(default=0)
    author_1_not_checked_messages_count = models.IntegerField(default=0)
    author_0_notifications = models.BooleanField(default=False)
    author_1_notifications = models.BooleanField(default=False)
    author_0_ban_chat = models.BooleanField(default=False)
    author_1_ban_chat = models.BooleanField(default=False)

    messages_count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.authors.all()[0]) + " & " + str(self.authors.all()[1])


class PrivateMessage(models.Model):
    private_chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000, default="no text")
    author = models.ForeignKey(Guest, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date created')

    is_answer = models.BooleanField(default=False)
    answer_for = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    answers_count = models.IntegerField(default=0)

    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author.name} ______ write: {self.text}"


"""class PublicChat(models.Model):
    name = models.CharField(max_length=100, default="no name")
    description = models.CharField(max_length=1000, default="no description")
    messages_count = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date created')
    participants = models.ManyToManyField(Guest)

    def __str__(self):
        return f"{self.name} ______ description: {self.description}"


class PublicMessage(models.Model):
    room_id = models.ForeignKey(PublicChat, on_delete=models.CASCADE)
    answer_for = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    message_text = models.CharField(max_length=2000, default="empty message")
    is_pinned = models.BooleanField(default=False)
    answers_count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.message_text)+" ______ room: "+str(self.room_id.name)

"""
"""class Group(models.Model):
    group_id=models.IntegerField()
    group_rooms=models."""