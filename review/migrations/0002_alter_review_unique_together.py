# Generated by Django 4.2.3 on 2023-08-16 13:44

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0004_alter_patient_summary'),
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('user', 'doctor')},
        ),
    ]