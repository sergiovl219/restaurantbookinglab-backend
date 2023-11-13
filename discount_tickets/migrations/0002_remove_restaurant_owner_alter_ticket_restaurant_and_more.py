# Generated by Django 4.2.7 on 2023-11-06 01:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
        ('discount_tickets', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='owner',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant'),
        ),
        migrations.DeleteModel(
            name='Owner',
        ),
        migrations.DeleteModel(
            name='Restaurant',
        ),
    ]
