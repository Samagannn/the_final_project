from django.db import models
from account.models import User
import json
from django.utils import timezone
from django_resized import ResizedImageField
from django.conf import settings


class Election(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class Candidate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, null=True, blank=True)
    bio = models.TextField()
    party = models.CharField(max_length=255, null=True, blank=True)
    photo = models.ImageField(upload_to='candidate_photos/', blank=True, null=True)
    votes_per_month = models.TextField(blank=True, default='{}')
    last_name = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)


class Voter(models.Model):
    address = models.CharField(max_length=255)
    has_voted = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.phone)


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
