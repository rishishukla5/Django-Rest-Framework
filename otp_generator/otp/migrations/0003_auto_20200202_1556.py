# Generated by Django 3.0.2 on 2020-02-02 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otp', '0002_otp_merchant_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otp',
            name='merchant_id',
        ),
        migrations.AlterField(
            model_name='otp',
            name='otp_generated',
            field=models.CharField(max_length=6, null=True),
        ),
    ]
