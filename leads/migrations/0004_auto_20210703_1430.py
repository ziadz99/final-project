# Generated by Django 3.1.4 on 2021-07-03 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0003_auto_20210703_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='organisation',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='leads.userprofile'),
        ),
    ]