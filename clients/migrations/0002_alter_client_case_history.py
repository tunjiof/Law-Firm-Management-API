# Generated by Django 4.2.16 on 2024-10-23 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='case_history',
            field=models.TextField(blank=True, null=True),
        ),
    ]
