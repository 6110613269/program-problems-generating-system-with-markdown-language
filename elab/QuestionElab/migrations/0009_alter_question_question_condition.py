# Generated by Django 3.2.9 on 2022-06-09 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuestionElab', '0008_question_question_element'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_condition',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
