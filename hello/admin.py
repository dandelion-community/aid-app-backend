from django.contrib import admin

from .models import AidRequest


class AidRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'what_is_needed',
        'completed',
        'who_is_it_for_freeform_text',
        'who_recorded_it_username',
        'zip_code',
        'who_is_it_for',
        'who_recorded_it',
    )


admin.site.register(AidRequest, AidRequestAdmin)
