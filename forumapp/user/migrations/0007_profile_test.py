# Generated by Django 3.2.9 on 2021-12-12 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20211212_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='test',
            field=models.CharField(default='test', max_length=22),
        ),
    ]