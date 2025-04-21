from django.db import models
from django.conf import settings
from django.utils import timezone

class Election(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    def __str__(self):
        return self.title

class Choice(models.Model):
    election = models.ForeignKey(Election, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='candidate_photos/', blank=True, null=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.text} ({self.votes})"

class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'election')  # Один пользователь — один голос
