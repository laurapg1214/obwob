# Generated by Django 5.1.1 on 2024-10-01 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obwob', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
