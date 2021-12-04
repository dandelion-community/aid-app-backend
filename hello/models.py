from django.contrib.auth.models import User
from django.db import models


class AnonymousPerson(models.Model):
    number = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )


class AidRequest(models.Model):
    what_is_needed = models.CharField(max_length=1000)
    completed = models.BooleanField(default=False)
    zip_code = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    who_is_it_for_freeform_text = models.CharField(
        max_length=100,
        null=True,
    )
    who_recorded_it_username = models.CharField(
        max_length=100,
        null=True,
    )
    who_is_it_for = models.ForeignKey(
        AnonymousPerson,
        on_delete=models.DO_NOTHING,
        related_name='requests_for',
        blank=True,
        null=True,
    )
    who_recorded_it = models.ForeignKey(
        AnonymousPerson,
        on_delete=models.DO_NOTHING,
        related_name='requests_recorded_by',
        blank=True,
        null=True
    )
