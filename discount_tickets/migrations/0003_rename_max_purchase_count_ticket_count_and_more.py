# Generated by Django 4.2.7 on 2023-11-06 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discount_tickets', '0002_remove_restaurant_owner_alter_ticket_restaurant_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='max_purchase_count',
            new_name='count',
        ),
        migrations.AddField(
            model_name='ticket',
            name='max_purchase',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
