# Generated by Django 2.1.5 on 2019-01-18 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0023_auto_20190118_0830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='card_number',
            field=models.CharField(max_length=50),
        ),
    ]