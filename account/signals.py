from django.db.models.signals import post_save
from django.dispatch import receiver
from rich import json

from election.models import Vote


@receiver(post_save, sender=Vote)
def update_votes_per_month(sender, instance, **kwargs):
    month = instance.timestamp.strftime('%Y-%m')
    candidate = instance.candidate

    if candidate.votes_per_month:
        votes_per_month = json.loads(candidate.votes_per_month)
    else:
        votes_per_month = {}

    votes_per_month[month] = votes_per_month.get(month, 0) + 1
    candidate.votes_per_month = json.dumps(votes_per_month)
    candidate.save()
