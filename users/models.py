from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # custom user model for later customization
    pass


class Preference(models.Model):
    class AIModels(models.TextChoices):
        GPT_3_5 = "gpt-3.5-turbo", "GPT-3.5"
        GEMINI_PRO = "gemini-pro", "Gemini Pro"

    SENTENCE_COUNT_CHOICES = tuple(zip(range(3, 11), range(3, 11)))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ai_model = models.CharField(
        max_length=20, choices=AIModels, default=AIModels.GPT_3_5
    )
    sentence_count = models.IntegerField(default=5, choices=SENTENCE_COUNT_CHOICES)
