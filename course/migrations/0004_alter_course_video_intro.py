# Generated by Django 4.1.1 on 2022-10-03 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_alter_lesson_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='video_intro',
            field=models.TextField(default='', max_length=1500),
        ),
    ]