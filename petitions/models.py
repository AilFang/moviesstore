from django.db import models
from django.contrib.auth.models import User

class Petition(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "pettions")
    created_at = models.DateTimeField(auto_now_add=True)

    def yes_count(self):
        return self.votes.filter(choice=Vote.CHOICE_YES).count()

    def no_count(self):
        return self.votes.filter(choice=Vote.CHOICE_NO).count()

    def __str__(self):
        return self.title
    
class Vote(models.Model):
    CHOICE_YES = 'yes'
    CHOICE_NO = 'no'
    CHOICES = [
        (CHOICE_YES, 'Yes'),
        (CHOICE_NO, 'No'),
    ]

    petition = models.ForeignKey(Petition, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='petition_votes')
    choice = models.CharField(max_length=10, choices=CHOICES)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('petition', 'user')  # one vote per user per petition