# Generated by Django 3.1 on 2021-07-03 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0011_auto_20210703_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='organisation',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='leads.userprofile'),
        ),
    ]
