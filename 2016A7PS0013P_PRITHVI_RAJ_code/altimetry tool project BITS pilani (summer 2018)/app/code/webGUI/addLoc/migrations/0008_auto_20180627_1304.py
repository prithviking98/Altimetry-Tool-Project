# Generated by Django 2.0.5 on 2018-06-27 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addLoc', '0007_auto_20180627_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='basin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='addLoc.Basin'),
        ),
    ]