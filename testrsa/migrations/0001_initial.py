# Generated by Django 2.0.4 on 2018-05-31 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n', models.TextField(verbose_name='n')),
                ('e', models.TextField(verbose_name='e')),
                ('d', models.TextField(verbose_name='d')),
                ('p', models.TextField(verbose_name='p')),
                ('q', models.TextField(verbose_name='q')),
            ],
        ),
    ]
