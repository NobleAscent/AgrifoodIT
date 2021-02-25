# Generated by Django 3.1.6 on 2021-02-25 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PresenceFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=200)),
                ('comments', models.CharField(max_length=200)),
                ('upload_date', models.DateTimeField(verbose_name='date uploaded')),
                ('processing_status', models.BooleanField()),
                ('upload', models.FileField(upload_to='uploads/presence/')),
            ],
        ),
    ]