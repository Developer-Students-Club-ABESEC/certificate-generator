# Generated by Django 3.1.3 on 2020-11-13 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificate', '0002_saveimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='saveimage',
            name='key',
            field=models.CharField(default='rajat', max_length=50, unique=True),
            preserve_default=False,
        ),
    ]
