from django.db import models
from django.contrib.auth.models import User


class Run(models.Model):
    STATUS_CHOICES = [
        ('init', 'Забег инициализирован'),
        ('in_progress', 'Забег начат'),
        ('finished', 'Забег закончен'),
    ]
    created_at = models.DateTimeField(auto_now=True)
    athlete = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='init')


class AthleteInfo(models.Model):
    user_id = models.OneToOneField(User, on_delete = models.CASCADE, primary_key=True)
    weight = models.IntegerField(null=True, blank=True)
    goals = models.TextField(null=True, blank=True)