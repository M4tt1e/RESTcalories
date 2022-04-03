# Generated by Django 4.0.3 on 2022-04-02 16:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cal', '0007_food_created_alter_food_name_counter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='counter',
            name='total_cal_day',
        ),
        migrations.AddField(
            model_name='counter',
            name='total_calories',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='counter',
            name='usr',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='counter',
            name='associated_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.RemoveField(
            model_name='counter',
            name='total_foods_day',
        ),
        migrations.AddField(
            model_name='counter',
            name='total_foods_day',
            field=models.ManyToManyField(blank=True, to='cal.food'),
        ),
    ]
