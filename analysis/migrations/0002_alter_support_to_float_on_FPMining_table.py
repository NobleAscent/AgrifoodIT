# Generated by Django 3.1.6 on 2021-04-22 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0001_create_table_for_fpmining'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fpmining',
            name='support',
            field=models.FloatField(),
        ),
    ]
