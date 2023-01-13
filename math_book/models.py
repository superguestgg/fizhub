from django.db import models
from django.utils import timezone


def su_cut(string, len_string):
    if len(string) > len_string:
        string = string[0:len_string]
    return string


class Guest(models.Model): #author
    guest_name = models.CharField(max_length=50, default="no name")
    guest_information = models.CharField(max_length=2000, default="no information")
    guest_password = models.CharField(max_length=50, default="1234")
    guest_icon_href = models.CharField(max_length=200, default="https://rkn.gov.ru/i/eagle_s.svg")
    guest_rights = models.IntegerField(default=0)
    subscriber_count = models.IntegerField(default=0)
    subscription_count = models.IntegerField(default=0)
    ticket_count = models.IntegerField(default=0)
    definition_count = models.IntegerField(default=0)
    theorem_count = models.IntegerField(default=0)
    color_theme = models.CharField(max_length=40, default="darkblue")

    def __str__(self):
        return self.guest_name


class Guest_session(models.Model): #author_session
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=100, default="its impossible")
    os = models.CharField(max_length=100, default='no name')
    computername = models.CharField(max_length=100, default='no name')
    HTTP_USER_AGENT = models.CharField(max_length=500, default='no name')

    def __str__(self):
        return str(self.guest) + " key: " + str(self.session_key)


class Subject(models.Model):
    subject_name = models.CharField(max_length=50, default="no name") #name_field#no_repeat
    subject_text = models.CharField(max_length=10000, default='no text') #information_field#no_repeat
    picture_href = models.CharField(max_length=100, default="https://rkn.gov.ru/i/eagle_s.svg")

    def __str__(self):
        return str(self.subject_name)+"__"+su_cut(str(self.subject_text), 50)


class University(models.Model):
    university_shortname = models.CharField(max_length=50, default="noshortname")
    university_name = models.CharField(max_length=100, default="no name") #name_field
    university_site = models.CharField(max_length=50, default="no link")
    university_text = models.CharField(max_length=10000, default='no text') #information_field
    picture_href = models.CharField(max_length=100, default="https://rkn.gov.ru/i/eagle_s.svg")

    def __str__(self):
        return str(self.university_name)+"__"+su_cut(str(self.university_text), 50)

class Ticket(models.Model):
    ticket_name = models.CharField(max_length=100, default='no name')
    by_guest = models.ForeignKey(Guest, on_delete=models.SET_DEFAULT, default=1)
    ticket_text = models.CharField(max_length=10000, default='no text')
    ticket_type_private = models.BooleanField(default=False)
    pub_date = models.DateTimeField('date published')
    university = models.ForeignKey(University, on_delete=models.SET_DEFAULT, default=1)
    study_direction = models.CharField(max_length=50, default="fiit")
    subject = models.ForeignKey(Subject, on_delete=models.SET_DEFAULT, default=1)
    vote_for_count = models.IntegerField(default=0) #autocomplete
    vote_against_count = models.IntegerField(default=0) #autocomplete
    picture_href = models.CharField(max_length=100, default="https://rkn.gov.ru/i/eagle_s.svg")

    def __str__(self):
        return (self.ticket_name + " text: " + self.ticket_text)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Vote_ticket(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    by_guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    vote_type = models.BooleanField(default=True)

class Session(models.Model):
    session_name = models.CharField(max_length=50, default="no name")
    session_text = models.CharField(max_length=10000, default="no text")
    by_guest = models.ForeignKey(Guest, on_delete=models.SET_DEFAULT, default=1)
    university = models.ForeignKey(University, on_delete=models.SET_DEFAULT, default=1)
    tickets = models.ManyToManyField(Ticket)

    def __str__(self):
        return str(self.session_name)+"__"+su_cut(str(self.session_text), 50)


class Theorem(models.Model):
    theorem_name = models.CharField(max_length=50, default="no name") #name
    by_guest = models.ForeignKey(Guest, on_delete=models.SET_DEFAULT, default=1) #author
    theorem_text = models.CharField(max_length=10000, default='no text') #text
    theorem_proof = models.CharField(max_length=10000, default='no text')
    pub_date = models.DateTimeField('date published') #pub_date
    subject = models.ForeignKey(Subject, on_delete=models.SET_DEFAULT, default=1)
    vote_for_count = models.IntegerField(default=0) #autocomplete
    vote_against_count = models.IntegerField(default=0) #autocomplete
    picture_href = models.CharField(max_length=100, default="https://rkn.gov.ru/i/eagle_s.svg") #image

    def __str__(self):
        return (self.theorem_name + " text: " + self.theorem_text)

    def get_html(self):
        return "<div class='theorem'> <center><div class='theorem_header'>теорема</div></center> <div class='theorem_header'>" + self.theorem_name+"</div>"+ self.theorem_text +"<div class='theorem_header'>доказательство:</div>" + self.theorem_proof +"</div>"



    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Vote_theorem(models.Model):
    theorem = models.ForeignKey(Theorem, on_delete=models.CASCADE)
    by_guest = models.ForeignKey(Guest, on_delete=models.CASCADE) #author
    vote_type = models.BooleanField(default=True)


class Definition(models.Model):
    definition_name = models.CharField(max_length=50, default="no name")
    by_guest = models.ForeignKey(Guest, on_delete=models.SET_DEFAULT, default=1)
    definition_text = models.CharField(max_length=10000, default='no text')
    pub_date = models.DateTimeField('date published')
    subject = models.ForeignKey(Subject, on_delete=models.SET_DEFAULT, default=1)
    vote_for_count = models.IntegerField(default=0) #autocomplete
    vote_against_count = models.IntegerField(default=0) #autocomplete
    picture_href = models.CharField(max_length=100, default="https://rkn.gov.ru/i/eagle_s.svg")

    def __str__(self):
        return (self.definition_name + " text: " + self.definition_text)

    def get_html(self):
        return "<div class='definition'> <center><div class='definition_header'>определение</div></center> <div class='definition_header'>" + self.definition_name + "</div>" + self.definition_text + "</div>"

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Vote_definition(models.Model):
    definition = models.ForeignKey(Definition, on_delete=models.CASCADE)
    by_guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    vote_type = models.BooleanField(default=True)


