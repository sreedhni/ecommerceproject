# Generated by Django 5.0.4 on 2024-04-11 22:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_review_order_delete_reviews'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='order',
        ),
    ]
