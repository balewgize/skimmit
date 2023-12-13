from django.db import models


class URLSummary(models.Model):
    """A class representing URL summary results."""

    url = models.URLField(max_length=500)
    title = models.CharField(max_length=250, blank=True)
    summary = models.TextField(blank=True)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"<URLSummary - {self.url}"
