# Generated by Django 3.2.9 on 2021-11-21 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Words',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oz', models.CharField(max_length=255, verbose_name="O'zbek")),
                ('en', models.CharField(max_length=255, verbose_name='Ingliz')),
            ],
            options={
                'verbose_name': "So'z",
                'verbose_name_plural': "So'zlar",
            },
        ),
    ]
