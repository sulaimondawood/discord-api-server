# Generated by Django 4.2.7 on 2023-12-27 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customuser_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, default='default-avatar.png', null=True, upload_to=''),
        ),
    ]
