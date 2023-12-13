from django.contrib import admin

from .models import URLSummary


@admin.register(URLSummary)
class URLSummaryAdmin(admin.ModelAdmin):
    list_display = ("url", "title", "created_at")
    search_fields = ("url", "title")
    list_filter = ("created_at",)
