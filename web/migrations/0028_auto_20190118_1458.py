# Generated by Django 2.1.5 on 2019-01-18 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0027_auto_20190118_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='card_number',
            field=models.CharField(max_length=50),
        ),
    ]
