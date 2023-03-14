# Generated by Django 3.1.14 on 2023-03-04 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20230303_1820'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='full_name',
        ),
        migrations.AddField(
            model_name='company',
            name='Company_name',
            field=models.CharField(default='Name', max_length=100),
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='full_name',
            field=models.CharField(default='Name', max_length=100),
        ),
    ]
