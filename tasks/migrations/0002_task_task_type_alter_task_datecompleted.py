# Generated by Django 5.1 on 2024-10-03 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='task_type',
            field=models.CharField(choices=[('normal', 'Normal'), ('urgent', 'Urgent')], default='normal', max_length=10),
        ),
        migrations.AlterField(
            model_name='task',
            name='datecompleted',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
