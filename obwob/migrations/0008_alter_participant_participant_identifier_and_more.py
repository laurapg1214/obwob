# Generated by Django 5.1.1 on 2024-10-08 20:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obwob', '0007_remove_organization_events_event_organizations_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='participant_identifier',
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
        migrations.CreateModel(
            name='ParticipantEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_participants', to='obwob.event')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participant_events', to='obwob.participant')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]