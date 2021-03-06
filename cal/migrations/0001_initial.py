# Generated by Django 4.0.3 on 2022-03-20 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Macros',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('protein', models.IntegerField()),
                ('carbs', models.IntegerField()),
                ('fat', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('calories', models.IntegerField()),
                ('favorite', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('macros', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cal.macros')),
            ],
        ),
    ]
