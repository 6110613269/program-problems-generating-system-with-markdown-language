# Generated by Django 3.2.9 on 2022-06-09 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuestionElab', '0007_question_question_condition'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_element',
            field=models.CharField(default=None, max_length=50),
        ),
    ]