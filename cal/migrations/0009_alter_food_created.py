# Generated by Django 4.0.3 on 2022-04-02 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0008_remove_counter_total_cal_day_counter_total_calories_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='created',
            field=models.DateField(auto_now_add=True),
        ),
    ]
