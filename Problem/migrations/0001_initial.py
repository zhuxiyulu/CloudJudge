# Generated by Django 2.0.1 on 2018-01-27 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('problemUrl', models.CharField(max_length=255)),
                ('source', models.CharField(max_length=100, null=True)),
                ('sourceUrl', models.CharField(max_length=255, null=True)),
                ('originalOJ', models.CharField(max_length=10)),
                ('originalProblem', models.CharField(max_length=20)),
                ('updateTime', models.DateTimeField()),
            ],
        ),
    ]