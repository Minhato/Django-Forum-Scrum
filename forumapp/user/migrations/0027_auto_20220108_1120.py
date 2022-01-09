# Generated by Django 3.2.9 on 2022-01-08 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0026_alter_reply_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.comment'),
        ),
        migrations.DeleteModel(
            name='Reply',
        ),
    ]
