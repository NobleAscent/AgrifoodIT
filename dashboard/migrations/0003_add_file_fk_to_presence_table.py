# Generated by Django 3.1.6 on 2021-03-24 22:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_seed_pig_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='presence',
            name='presence_file',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='dashboard.presencefile'),
            preserve_default=False,
        ),
    ]
