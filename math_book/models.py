from django.db import models
from django.utils import timezone


def su_cut(string, len):
    if len(string) > len:
        string = string[0:len]
    return string


class Guest(models.Model):
    guest_name = models.CharField(max_length=50)
    guest_information = models.CharField(max_length=2000, default="no information")
    guest_password = models.CharField(max_length=50, default="1234")
    guest_icon_href = models.CharField(max_length=200,
                                       default="https://ustanovkaos.ru/wp-content/uploads/2022/02/06-psevdo-pustaya-ava.jpg")
    guest_rights = models.IntegerField(default=0)
    subscriber_count = models.IntegerField(default=0)
    subscription_count = models.IntegerField(default=0)
    ticket_count = models.IntegerField(default=0)
    definition_count = models.IntegerField(default=0)
    theorem_count = models.IntegerField(default=0)
    color_theme = models.CharField(max_length=40, default="darkblue")

    def __str__(self):
        return self.guest_name


class Guest_session(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=100)
    os = models.CharField(max_length=100, default='no name')
    computername = models.CharField(max_length=100, default='no name')
    HTTP_USER_AGENT = models.CharField(max_length=500, default='no name')

    def __str__(self):
        return str(self.guest) + " key: " + str(self.session_key)


class Subject(models.Model):
    subject_name = models.CharField(max_length=50, default="no name")
    subject_description = models.CharField(max_length=5000, default='no description')
    picture_href = models.CharField(max_length=100, default="https://rkn.gov.ru/")

    def __str__(self):
        return str(self.subject_name)+"__"+su_cut(str(self.subject_description), 50)


class University(models.Model):
    university_shortname = models.CharField(max_length=50, default="noshortname")
    university_name = models.CharField(max_length=100, default="no name")
    university_site = models.CharField(max_length=50, default="no link")
    university_description = models.CharField(max_length=5000, default='no description')
    picture_href = models.CharField(max_length=100, default="https://rkn.gov.ru/")

    def __str__(self):
        return str(self.university_name)+"__"+su_cut(str(self.university_description), 50)

class Ticket(models.Model):
    ticket_name = models.CharField(max_length=100, default='no name')
    author = models.ForeignKey(Guest, on_delete=models.CASCADE, default=1)
    ticket_text = models.CharField(max_length=10000, default='no text')
    ticket_type_private = models.BooleanField(default=False)
    pub_date = models.DateTimeField('date published')
    university_name = models.ForeignKey(University, on_delete=models.SET_NULL)
    study_direction = models.CharField(max_length=50, default="fiit")
    subject_name = models.ForeignKey(Subject, on_delete=models.SET_NULL, default=1)
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    picture_href = models.CharField(max_length=100, default="https://rkn.gov.ru/")

    def __str__(self):
        return (self.ticket_name + " text: " + self.ticket_text)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Like(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)

class Dislike(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)


class Session_tickets(models.Model):
    session_name = models.CharField(max_length=50, default="no name")
    session_description = models.CharField(max_length=5000, default="no description")
    author = models.ForeignKey(Guest, on_delete=models.CASCADE, default=1)
    university = models.ForeignKey(University, on_delete=models.SET_NULL)
    tickets = models.ManyToManyField(Ticket)

    def __str__(self):
        return str(self.session_name)+"__"+su_cut(str(self.session_description), 50)


class Theorem(models.Model):
    theorem_name = models.CharField(max_length=50, default="no name")
    author = models.ForeignKey(Guest, on_delete=models.CASCADE, default=1)
    theorem_text = models.CharField(max_length=10000, default='no text')
    pub_date = models.DateTimeField('date published')
    subject_name = models.ForeignKey(Subject, on_delete=models.SET_NULL, default=1)
    vote_for_count = models.IntegerField(default=0)
    vote_against_count = models.IntegerField(default=0)
    picture_href = models.CharField(max_length=100, default="https://rkn.gov.ru/")

    def __str__(self):
        return (self.theorem_name + " text: " + self.theorem_text)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Vote_theorem(models.Model):
    theorem = models.ForeignKey(Theorem, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    vote_type = models.BooleanField(default=True)


class Definition(models.Model):
    definition_name = models.CharField(max_length=50, default="no name")
    author = models.ForeignKey(Guest, on_delete=models.CASCADE, default=1)
    definition_text = models.CharField(max_length=10000, default='no text')
    pub_date = models.DateTimeField('date published')
    subject_name = models.ForeignKey(Subject, on_delete=models.SET_NULL, default=1)
    vote_for_count = models.IntegerField(default=0)
    vote_against_count = models.IntegerField(default=0)
    picture_href = models.CharField(max_length=100, default="https://rkn.gov.ru/")

    def __str__(self):
        return (self.definition_name + " text: " + self.definition_text)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Vote_definition(models.Model):
    definition = models.ForeignKey(Definition, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    vote_type = models.BooleanField(default=True)


