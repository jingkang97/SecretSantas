# Generated by Django 3.2.4 on 2021-07-03 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secretsanta', '0004_group_shuffled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gift',
            name='category',
        ),
        migrations.AddField(
            model_name='gift',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='gift_category', to='secretsanta.Category'),
        ),
    ]
