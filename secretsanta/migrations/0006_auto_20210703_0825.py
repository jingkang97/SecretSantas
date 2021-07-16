# Generated by Django 3.2.4 on 2021-07-03 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secretsanta', '0005_auto_20210703_0542'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='group',
        ),
        migrations.AddField(
            model_name='user',
            name='group',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_group', to='secretsanta.Group'),
        ),
    ]
