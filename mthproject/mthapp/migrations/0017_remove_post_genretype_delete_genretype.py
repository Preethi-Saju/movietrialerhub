# Generated by Django 4.2.11 on 2024-04-30 02:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mthapp', '0016_rename_typegenre_post_genretype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='genretype',
        ),
        migrations.DeleteModel(
            name='GenreType',
        ),
    ]
