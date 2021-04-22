# Generated by Django 3.1.6 on 2021-04-22 23:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dashboard', '0004_add_weather_models'),
    ]

    operations = [
        migrations.CreateModel(
            name='FPMining',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('support', models.IntegerField()),
                ('itemset', models.CharField(max_length=200)),
                ('pig', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.pig')),
            ],
        ),
    ]
