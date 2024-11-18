# Generated by Django 4.2.14 on 2024-07-23 05:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0005_remove_student_booked_hostel_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='booked_hostel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hostel.hostel'),
        ),
        migrations.AddField(
            model_name='student',
            name='booked_room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hostel.room'),
        ),
    ]
