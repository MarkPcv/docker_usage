# Generated by Django 4.2.4 on 2023-08-22 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_telegram_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='telegram_id',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='telegram_id'),
        ),
    ]
