# Generated by Django 3.1.7 on 2021-02-23 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20210221_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='option',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.options', verbose_name='Выбранные вариант ответа'),
        ),
    ]
