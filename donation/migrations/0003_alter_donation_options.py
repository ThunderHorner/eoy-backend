# Generated by Django 5.1.4 on 2024-12-05 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0002_alter_donation_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='donation',
            options={'ordering': ('-created_at',)},
        ),
    ]
