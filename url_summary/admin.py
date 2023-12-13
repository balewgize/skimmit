from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import URLSummary


@admin.register(URLSummary)
class URLSummaryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """Admin View for URL Summary."""

    list_display = ("url", "title", "created_at")
    search_fields = ("url", "title")
    list_filter = ("created_at",)
