# Generated by Django 5.0.1 on 2024-01-23 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254, unique=True),
        ),
    ]
