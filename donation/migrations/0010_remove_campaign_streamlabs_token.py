# Generated by Django 5.1.4 on 2024-12-06 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0009_alter_campaign_streamlabs_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='streamlabs_token',
        ),
    ]
