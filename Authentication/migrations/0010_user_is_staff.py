# Generated by Django 2.0.1 on 2018-01-30 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0009_auto_20180129_0811'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.IntegerField(default=0, verbose_name='is_staff'),
        ),
    ]
