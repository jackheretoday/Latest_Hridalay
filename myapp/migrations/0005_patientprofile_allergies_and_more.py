# Generated by Django 4.2.19 on 2025-04-13 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_doctorprofile_available_days_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientprofile',
            name='allergies',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='current_medications',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='emergency_contact',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='emergency_phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='emergency_relationship',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='last_checkup',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='patient_profiles/'),
        ),
    ]
