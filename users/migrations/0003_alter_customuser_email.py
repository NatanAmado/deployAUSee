# Generated by Django 4.2.7 on 2024-01-10 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_major_customuser_track'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(default='NA', max_length=254, unique=False),
        ),
    ]
