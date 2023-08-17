# Generated by Django 4.2.4 on 2023-08-17 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import myApp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInformation',
            fields=[
                ('id', models.UUIDField(default=myApp.models.get_uuid, primary_key=True, serialize=False, unique=True)),
                ('profile', models.ImageField(default='avatar.png', upload_to='profile/')),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('type', models.CharField(choices=[('Doctor', 'Doctor'), ('Patient', 'Patient')], default=('Doctor', 'Doctor'), max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]