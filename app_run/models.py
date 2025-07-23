from django.contrib.auth.models import User
from django.db import models


class Run(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    athlete = models.ForeignKey(User, on_delete=models.CASCADE, related_name='runs')
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Забег #{self.pk} ({str(self.athlete)})"
