# Generated by Django 5.1.3 on 2024-11-19 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_alter_usersignup_address_alter_usersignup_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersignup',
            name='role',
            field=models.CharField(blank=True, choices=[('Admin', 'Admin'), ('Consumer', 'Consumer'), ('Tricycler', 'Tricycler')], max_length=200, null=True),
        ),
    ]
