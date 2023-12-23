from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Preference


class CustomUserAdmin(UserAdmin):
    model = User


admin.site.register(User, CustomUserAdmin)


@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):
    list_display = ["user", "ai_model", "sentence_length"]
    list_filter = ["ai_model"]
