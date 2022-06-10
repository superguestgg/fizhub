from django.db import models
class Guest(models.Model):
    guest_name = models.CharField(max_length=40)
    guest_information = models.CharField(max_length=2000, default="no information")
    guest_password = models.CharField(max_length=40, default="1234")
    guest_rights = models.IntegerField(default=0)

    def __str__(self):
        return self.guest_name
class Guest_session(models.Model):
    guest_id = models.ForeignKey(Guest, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=100)
    def __str__(self):
        return str(self.guest_id)+" key: "+str(self.session_key)
class Task(models.Model):
    task_name = models.CharField(max_length=50, default='no name')
    task_text = models.CharField(max_length=1500)
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
"""class Olympiad(models.Model):
    olympiad_name = models.CharField(max_length=100, default="no name")
    olympiad_description = models.CharField(max_length=2000, default="no name")
"""