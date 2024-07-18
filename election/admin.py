from django.contrib import admin
from election.models import Election, Candidate, Voter, Vote

admin.site.register(Election)
admin.site.register(Candidate)
admin.site.register(Voter)
admin.site.register(Vote)

# Register your models here.
