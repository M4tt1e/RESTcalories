# Generated by Django 4.0.3 on 2022-04-02 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0010_remove_counter_total_foods_day_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='counter',
            name='total_foods_day',
        ),
        migrations.AddField(
            model_name='counter',
            name='total_foods_day',
            field=models.ManyToManyField(to='cal.food'),
        ),
    ]