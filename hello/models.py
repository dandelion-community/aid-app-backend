from django.db import models


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
