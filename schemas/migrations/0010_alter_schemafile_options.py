# Generated by Django 3.2.2 on 2021-05-18 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schemas', '0009_alter_schemamodel_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schemafile',
            options={'ordering': ['-created_at']},
        ),
    ]