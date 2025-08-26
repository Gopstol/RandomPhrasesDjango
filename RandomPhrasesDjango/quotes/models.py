from django.db import models
from django.contrib.auth.models import User


class Quote(models.Model):
    text = models.TextField(unique=True)
    source = models.CharField(max_length=255)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quotes")
    weight = models.IntegerField()

    def __str__(self):
        return f"{self.text[:50]}... ({self.source})"
