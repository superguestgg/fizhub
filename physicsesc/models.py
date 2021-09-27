from django.db import models
class Guest(models.Model):
    guest_name = models.CharField(max_length=40)
class Task(models.Model):
    task_text = models.CharField(max_length=1000)
    pub_date = models.DateTimeField('date published')
    class_name = models.CharField(max_length=20, default="11")
    theme1_name = models.CharField(max_length=30, default="No theme")
    theme2_name = models.CharField(max_length=30, default="No theme")
    creator_name = models.ForeignKey(Guest, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return self.task_text
    def was_published_recently(self):
        return self.pub_date>=timezone.now()-datetime.timedelta(days=1)

class Solution(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    solution_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.solution_text
