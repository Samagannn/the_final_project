from django.db import models
from account.models import User
import json
from django.utils import timezone


class Election(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


class Candidate(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    party = models.CharField(max_length=255)
    bio = models.TextField()
    votes_per_month = models.TextField(default='{}')

    def __str__(self):
        return self.name


class Voter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


class Vote(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        month = self.timestamp.strftime('%Y-%m')
        candidate = self.candidate

        if candidate.votes_per_month:
            votes_per_month = json.loads(candidate.votes_per_month)
        else:
            votes_per_month = {}

        votes_per_month[month] = votes_per_month.get(month, 0) + 1
        candidate.votes_per_month = json.dumps(votes_per_month)
        candidate.save()

# Create your models here.
