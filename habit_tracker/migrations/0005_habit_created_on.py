# Generated by Django 4.2.4 on 2023-08-22 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habit_tracker', '0004_alter_habit_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='created_on',
            field=models.DateField(auto_now_add=True, default='2023-08-21', verbose_name='created_on'),
            preserve_default=False,
        ),
    ]