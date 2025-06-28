from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


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
    distance = models.FloatField(default=True, blank=True)


class AthleteInfo(models.Model):
    user_id = models.OneToOneField(User, on_delete = models.CASCADE, primary_key=True)
    weight = models.IntegerField(null=True, blank=True)
    goals = models.TextField(null=True, blank=True)


class Challenge(models.Model):
    full_name = models.TextField()
    athlete = models.ForeignKey(User, on_delete=models.CASCADE)


class Position(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=4, validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)])
    longitude = models.DecimalField(max_digits=9, decimal_places=4, validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])


class CollectibleItem(models.Model):
    name = models.TextField()
    uid = models.CharField(max_length=15)
    latitude = models.DecimalField(max_digits=9, decimal_places=4, validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)])
    longitude = models.DecimalField(max_digits=9, decimal_places=4, validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])
    picture = models.URLField()
    value = models.IntegerField()
    users = models.ManyToManyField(User, blank=True,
                                   related_name='collectible_items')