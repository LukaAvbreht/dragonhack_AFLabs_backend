# Generated by Django 3.1.3 on 2020-11-07 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pasovcek', '0003_auto_20201107_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='nesreca',
            name='lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='nesreca',
            name='long',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
