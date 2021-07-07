# Generated by Django 3.2.4 on 2021-06-23 09:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='searchdb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=20)),
                ('locality', models.CharField(max_length=30)),
                ('shopname', models.CharField(max_length=100)),
                ('shopaddress', models.CharField(max_length=500)),
                ('shopcontact', models.CharField(max_length=12)),
                ('shopimage', models.ImageField(upload_to='searchdb/')),
                ('is_verified', models.BooleanField(default=False)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
