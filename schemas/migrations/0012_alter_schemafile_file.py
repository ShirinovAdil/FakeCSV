# Generated by Django 3.2.2 on 2021-05-18 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schemas', '0011_alter_schemafile_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schemafile',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='media/', verbose_name='Schema'),
        ),
    ]
