# Generated by Django 3.1.7 on 2021-05-08 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_company_bse_code'),
        ('stock', '0002_stock_created_at'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='stock',
            unique_together={('company', 'record_date')},
        ),
    ]