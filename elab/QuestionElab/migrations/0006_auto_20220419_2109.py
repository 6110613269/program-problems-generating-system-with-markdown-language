# Generated by Django 3.2.12 on 2022-04-19 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuestionElab', '0005_auto_20220419_2104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='username',
        ),
        migrations.AddField(
            model_name='question',
            name='question_username',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
