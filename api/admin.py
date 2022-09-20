from django.contrib import admin
import api.models


@admin.register(api.models.Reading)
class MeterReadingAdmin(admin.ModelAdmin):
    list_display = (
        "mpan_core",
        "register_id",
        "meter_id",
        "reading_value",
        "reading_taken_at",
        "reading_flag",
        "reading_method",
        "file_name",
    )
    search_fields = (
        "mpan_core__mpan_core__startswith",
        "meter_id__id__startswith",
    )
