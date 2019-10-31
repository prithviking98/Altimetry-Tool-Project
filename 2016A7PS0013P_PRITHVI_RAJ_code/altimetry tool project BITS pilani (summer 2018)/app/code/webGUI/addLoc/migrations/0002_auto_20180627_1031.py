# Generated by Django 2.0.5 on 2018-06-27 05:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addLoc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Satellite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameShort', models.CharField(max_length=5, unique=True)),
                ('nameLong', models.CharField(max_length=25, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='location',
            name='satellite',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='addLoc.Satellite'),
            preserve_default=False,
        ),
    ]