# Generated by Django 2.2.16 on 2022-08-12 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_confirmation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(max_length=6, null=True, verbose_name='confirmation_code'),
        ),
    ]