# Generated by Django 3.2.5 on 2021-12-31 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_merge_20211230_1154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
