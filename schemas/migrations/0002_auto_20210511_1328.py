# Generated by Django 3.2.2 on 2021-05-11 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schemas', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schema',
            options={'verbose_name': 'Schema', 'verbose_name_plural': 'Schemas'},
        ),
        migrations.AddField(
            model_name='schema',
            name='separator',
            field=models.CharField(default=',', max_length=1, verbose_name='Separator'),
        ),
    ]
