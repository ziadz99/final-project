# Generated by Django 3.1.4 on 2021-07-03 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0005_auto_20210703_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='organisation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='leads.userprofile'),
            preserve_default=False,
        ),
    ]
