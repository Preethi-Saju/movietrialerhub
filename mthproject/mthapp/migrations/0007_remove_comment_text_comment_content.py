# Generated by Django 4.2.11 on 2024-04-26 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mthapp', '0006_remove_profile_id_profile_id_user_alter_profile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='text',
        ),
        migrations.AddField(
            model_name='comment',
            name='content',
            field=models.TextField(default='', max_length=150),
        ),
    ]