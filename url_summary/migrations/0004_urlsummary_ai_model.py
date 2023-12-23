# Generated by Django 5.0 on 2023-12-23 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('url_summary', '0003_urlsummary_bookmarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='urlsummary',
            name='ai_model',
            field=models.CharField(blank=True, choices=[('gpt-3.5-turbo', 'GPT-3.5'), ('gemini-pro', 'Gemini Pro')], max_length=20, null=True),
        ),
    ]
