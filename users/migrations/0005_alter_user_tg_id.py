# Generated by Django 3.2.9 on 2021-12-15 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20211215_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='tg_id',
            field=models.BigIntegerField(default=0),
        ),
    ]
