# Generated by Django 3.1.7 on 2021-05-07 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_date', models.DateTimeField(default=None, null=True)),
                ('open', models.FloatField(default=-1)),
                ('high', models.FloatField(default=-1)),
                ('low', models.FloatField(default=-1)),
                ('close', models.FloatField(default=-1)),
                ('volume', models.FloatField(default=-1)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company')),
            ],
        ),
    ]
