# Generated by Django 5.0 on 2023-12-23 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_preference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preference',
            name='sentence_length',
            field=models.IntegerField(choices=[(3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=5),
        ),
    ]