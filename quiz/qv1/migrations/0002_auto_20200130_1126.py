# Generated by Django 3.0.2 on 2020-01-30 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qv1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='dob',
            field=models.DateField(auto_created=True),
        ),
    ]
