# Generated by Django 5.0.7 on 2024-07-10 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostel',
            name='image_url',
            field=models.URLField(default='https://example.com/default-hostel-image.jpg'),
        ),
    ]