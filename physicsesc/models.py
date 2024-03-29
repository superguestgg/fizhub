from django.db import models
from django.utils import timezone
def su_cut(string, l):
    if len(string) > l:
        string = string[0:l]
    return string
class Guest(models.Model):
    guest_name = models.CharField(max_length=40)
    guest_information = models.CharField(max_length=2000, default="no information")
    guest_password = models.CharField(max_length=40, default="1234")
    guest_icon_href = models.CharField(max_length=200, default="https://ustanovkaos.ru/wp-content/uploads/2022/02/06-psevdo-pustaya-ava.jpg")
    guest_rights = models.IntegerField(default=0)
    subscriber_count = models.IntegerField(default=0)
    subscription_count = models.IntegerField(default=0)
    task_count = models.IntegerField(default=0)
    article_count = models.IntegerField(default=0)
    color_theme = models.CharField(max_length=40, default="darkblue")
    def __str__(self):
        return self.guest_name
class Guest_session(models.Model):
    guest_id = models.ForeignKey(Guest, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=100)
    os = models.CharField(max_length=100, default='no name')
    computername = models.CharField(max_length=100, default='no name')
    HTTP_USER_AGENT = models.CharField(max_length=500, default='no name')
    def __str__(self):
        return str(self.guest_id)+" key: "+str(self.session_key)
class Subscription(models.Model):
    author_id = models.IntegerField(default=1)
    subscriber = models.ForeignKey(Guest, on_delete=models.CASCADE)


class Private_chat(models.Model):
    authors = models.ManyToManyField(Guest)
    author_1_not_checked_messages_count = models.IntegerField(default=0)
    author_2_not_checked_messages_count = models.IntegerField(default=0)
    def __str__(self):
        return str(self.authors.all()[0])+" & "+str(self.authors.all()[1])

class Private_message(models.Model):
    is_answer = models.BooleanField(default=False)
    answer_for = models.CharField(default="", max_length=3000)
    answer_for_id = models.IntegerField(default=0)
    private_chat = models.ForeignKey(Private_chat, on_delete=models.CASCADE)
    author = models.ForeignKey(Guest, on_delete=models.CASCADE)
    message_text = models.CharField(max_length=3000, default="no text")
    pub_date = models.DateTimeField('date published')
    is_read = models.BooleanField(default=False)
    def __str__(self):
        return str(self.private_chat)+":___"+str(su_cut(self.message_text,50))

class Task(models.Model):
    task_name = models.CharField(max_length=50, default='no name')
    task_text = models.CharField(max_length=3000)
    task_type_private = models.BooleanField(default=False)
    pub_date = models.DateTimeField('date published')
    class_name = models.CharField(max_length=20, default="11")
    theme1_name = models.CharField(max_length=30, default="No theme")
    theme2_name = models.CharField(max_length=30, default="No theme")
    creator_name = models.ForeignKey(Guest, on_delete=models.CASCADE, default=1)
    like_count = models.IntegerField(default=0)
    report_count = models.IntegerField(default=0)
    picture_href = models.CharField(max_length=100, default="https://rkn.gov.ru/")
    def __str__(self):
        return (self.task_name + " text: " + self.task_text)
    def was_published_recently(self):
        return self.pub_date>=timezone.now()-datetime.timedelta(days=1)

class Like(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
class Report(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
class Solution(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    creator_id = models.ForeignKey(Guest, on_delete=models.CASCADE, default=1)
    solution_text = models.CharField(max_length=500)
    votes_count = models.IntegerField(default=0)
    votes_against_count = models.IntegerField(default=0)
    def __str__(self):
        return self.solution_text
class Vote(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    vote_type = models.BooleanField(default=True)
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)

class Usefulfiles(models.Model):
    file_name=models.CharField(max_length=50, default="no name")
    creator_id=models.ForeignKey(Guest, on_delete=models.CASCADE)
    file_href=models.CharField(max_length=200, default="no name")
    def __str__(self):
        return self.file_name

class Group(models.Model):
    group_name = models.CharField(max_length=50, default='no name')
    author = models.ForeignKey(Guest, on_delete=models.CASCADE)
    author_helper_count = models.IntegerField(default=0)
    group_description = models.CharField(default="no description", max_length=3000)
    group_type_password = models.BooleanField(default=False)
    group_password = models.CharField(max_length=50, default="1234")
    group_private_type = models.BooleanField(default=False)
    group_application_type = models.BooleanField(default=False)
    student_count = models.IntegerField(default=0)
    group_theme_count = models.IntegerField(default=1)
    picture_href = models.CharField(max_length=100, default="https://rkn.gov.ru/")
    def __str__(self):
        return (self.group_name + " description: " + self.group_description)
class Group_theme(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    group_theme_name = models.CharField(max_length=50, default="no name")
    task_count = models.IntegerField(default=0)
    group_theme_description = models.CharField(default="no description", max_length=3000)
class Group_task(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    group_theme = models.ForeignKey(Group_theme, on_delete=models.CASCADE)
    task_comment = models.CharField(max_length=50, default="no comment")
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
class Group_student(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    student = models.ForeignKey(Guest, on_delete=models.CASCADE)
    application_type = models.BooleanField(default=False)
class Group_author_helper(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    author_helper = models.ForeignKey(Guest, on_delete=models.CASCADE)
    application_type = models.BooleanField(default=False)



class Article(models.Model):
    author = models.ForeignKey(Guest, on_delete=models.CASCADE)
    article_name = models.CharField(max_length=50, default="no name")
    article_theme1_name = models.CharField(max_length=50, default="no name")
    article_theme2_name = models.CharField(max_length=50, default="no name")
    article_page_count = models.IntegerField(default=0)
    article_vote_count = models.IntegerField(default=0)
    article_vote_against_count = models.IntegerField(default=0)
    article_private_type = models.BooleanField(default=False)
    article_description = models.CharField(max_length=3000, default="no name")
    def __str__(self):
        return str(self.article_name)+" by "+str(self.author)
class Article_vote(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    vote_type = models.BooleanField(default=True)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.vote_type)+ " for "+str(self.article)
class Article_page(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    article_page_name = models.CharField(max_length=50, default="no name")
    article_page_number = models.IntegerField(default=1)
    article_page_text = models.CharField(max_length=3000, default="no name")
    def __str__(self):
        return str(self.article_page_name)+" from "+str(self.article)



class Olympiad(models.Model):
    olympiad_name = models.CharField(max_length=100, default="no name")
    olympiad_description = models.CharField(max_length=2000, default="no information")
    olympiad_site_link = models.CharField(max_length=200, default="no link")
    olympiad_part_count = models.IntegerField(default=1)
    olympiad_author = models.ForeignKey(Guest, on_delete=models.CASCADE)
    olympiad_participant_count = models.IntegerField(default=0)
    olympiad_level = models.IntegerField(default=4)
    olympiad_class_name = models.IntegerField(default=11)
class Olympiad_part(models.Model):
    olympiad = models.ForeignKey(Olympiad, on_delete=models.CASCADE)
    olympiad_part_description = models.CharField(max_length=2000, default="no information")
    olympiad_part_site_link = models.CharField(max_length=200, default="no link")
    olympiad_part_number = models.IntegerField(default=1)
    olympiad_task_count = models.IntegerField(default=1)
    olympiad_part_participant_count = models.IntegerField(default=0)
class Olympiad_task(models.Model):
    olympiad = models.ForeignKey(Olympiad, on_delete=models.CASCADE)
    olympiad_part = models.ForeignKey(Olympiad_part, on_delete=models.CASCADE)
    task_number = models.IntegerField(default=1)
    task_name = models.CharField(max_length=50, default='no name')
    task_text = models.CharField(max_length=3000)
    pub_date = models.DateTimeField('date published')
    task_score = models.IntegerField(default=1)
    theme1_name = models.CharField(max_length=30, default="No theme")
    theme2_name = models.CharField(max_length=30, default="No theme")
    creator_name = models.ForeignKey(Guest, on_delete=models.CASCADE, default=1)
    picture_href = models.CharField(max_length=100, default="https://rkn.gov.ru/")
    def __str__(self):
        return (self.task_name + " text: " + self.task_text)
"""class Olympiad_participant(models.Model):
    olympiad = models.ForeignKey(Olympiad, on_delete=models.CASCADE)
    participant = models.ForeignKey(Guest, on_delete=models.CASCADE)
    olympiad_part_number = models.IntegerField(default=1)
    olympiad_participant_condition = models.CharField(max_length=30, default="No theme")
"""