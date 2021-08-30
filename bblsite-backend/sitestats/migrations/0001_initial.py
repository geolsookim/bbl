# Generated by Django 3.2.6 on 2021-08-30 13:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteStat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.CharField(choices=[('login', 'Login'), ('logout', 'Logout')], max_length=10)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, help_text='The time at which the first visit of the day was recorded')),
            ],
        ),
    ]
