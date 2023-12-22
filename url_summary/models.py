from django.db import models
from django.conf import settings


class URLSummary(models.Model):
    """A class representing URL summary results."""

    url = models.URLField(max_length=500)
    title = models.CharField(max_length=250, blank=True)
    summary = models.TextField(blank=True)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    bookmarks = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="bookmarked_summaries",
        blank=True,
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "URL Summary"

    def __str__(self) -> str:
        return f"<URLSummary - {self.url}"
