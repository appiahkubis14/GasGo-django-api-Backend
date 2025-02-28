# Generated by Django 5.1.3 on 2024-11-19 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('authentication', '0005_alter_usersignup_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersignup',
            name='groups',
            field=models.ManyToManyField(blank=True, to='auth.group'),
        ),
        migrations.AlterField(
            model_name='usersignup',
            name='hostel',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='usersignup',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
        migrations.AlterField(
            model_name='usersignup',
            name='photo',
            field=models.ImageField(default='users/photo/default.png', upload_to='users/photo/'),
        ),
        migrations.AlterField(
            model_name='usersignup',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, to='auth.permission'),
        ),
    ]
