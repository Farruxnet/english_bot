# Generated by Django 3.2.9 on 2021-12-15 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_auto_20211215_0742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='words',
            name='en',
            field=models.CharField(max_length=255, verbose_name='Ingliz'),
        ),
    ]
