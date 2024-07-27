from django.contrib import admin
from election.models import Election, Candidate, Voter, Vote

admin.site.register(Election)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('party', 'bio')
    search_fields = ('party',)


admin.site.register(Voter)
admin.site.register(Vote)

# Register your models here.
