# Generated by Django 4.2 on 2023-07-07 04:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('designers', '__first__'),
        ('services', '0001_initial'),
        ('companies', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='favoritecompany',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='companygallery',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gallery', to='companies.company'),
        ),
        migrations.AddField(
            model_name='company',
            name='designers',
            field=models.ManyToManyField(blank=True, related_name='designers', to='designers.designer'),
        ),
        migrations.AddField(
            model_name='company',
            name='packages',
            field=models.ManyToManyField(blank=True, related_name='packages', to='companies.package'),
        ),
        migrations.AddField(
            model_name='company',
            name='services',
            field=models.ManyToManyField(blank=True, related_name='company', to='services.services'),
        ),
    ]