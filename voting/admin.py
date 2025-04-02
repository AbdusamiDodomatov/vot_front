from django.contrib import admin
from .models import Election, Candidate, ElectionVote, Poll, Choice, PollVote

admin.site.register(Election)
admin.site.register(Candidate)
admin.site.register(ElectionVote)
admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(PollVote)
