# Generated by Django 5.1.4 on 2024-12-05 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0006_donation_tx_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='currency',
            field=models.CharField(default='ETH', max_length=100),
            preserve_default=False,
        ),
    ]
