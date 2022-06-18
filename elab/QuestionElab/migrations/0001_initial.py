# Generated by Django 3.2.12 on 2022-03-22 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(max_length=4)),
                ('course_name', models.CharField(max_length=20)),
                ('course_details', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_id', models.CharField(max_length=4)),
                ('question_type', models.CharField(max_length=1)),
                ('question_language', models.CharField(max_length=1)),
                ('question_source', models.TextField()),
                ('question_html', models.TextField()),
                ('question_answer', models.TextField()),
                ('question_course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='QuestionElab.course')),
            ],
        ),
    ]