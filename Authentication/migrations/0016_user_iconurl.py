# Generated by Django 2.0.2 on 2018-02-06 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0015_remove_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='iconUrl',
            field=models.CharField(max_length=300, null=True, verbose_name='iconUrl'),
        ),
    ]
