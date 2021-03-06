# Generated by Django 2.2.7 on 2020-04-08 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Metadata',
            fields=[
                ('node_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('Building_Name', models.CharField(null=True, max_length=255)),
                ('Start_Date', models.DateField(null=True)),
                ('Consumption', models.CharField(null=True, max_length=255)),
                ('Units', models.CharField(null=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='YearlyResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('node_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='downloadcsv.Metadata')),
            ],
        ),
    ]
