# Generated by Django 2.0.5 on 2018-06-27 05:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addLoc', '0002_auto_20180627_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='satellite',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='addLoc.Satellite'),
        ),
    ]