# Generated by Django 5.0.1 on 2024-01-22 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentoPDF',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('archivo', models.FileField(upload_to='documentos_pdf/')),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
