# Generated by Django 3.2.3 on 2021-07-07 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0021_agent_salary'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='position',
            field=models.CharField(default='sales person', max_length=20),
            preserve_default=False,
        ),
    ]
