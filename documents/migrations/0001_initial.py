# Generated by Django 4.2.16 on 2024-10-01 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cases', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=255)),
                ('file_type', models.CharField(max_length=50)),
                ('uploaded_date', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(upload_to='documents/')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='cases.case')),
            ],
        ),
    ]
