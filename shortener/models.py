from django.db import models
from django.contrib.auth.models import User


class Link(models.Model):
    client = models.ForeignKey(User, blank=True, null=True, related_name='workers', on_delete=models.DO_NOTHING)
    old_link = models.CharField(max_length=100, verbose_name="original_link")
    new_link = models.CharField(max_length=20, verbose_name="new_link")
