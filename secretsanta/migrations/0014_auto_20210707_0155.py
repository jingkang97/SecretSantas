# Generated by Django 3.2.4 on 2021-07-07 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secretsanta', '0013_like_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='gifts',
        ),
        migrations.AddField(
            model_name='wishlist',
            name='gifts',
            field=models.ManyToManyField(blank=True, null=True, related_name='wishlist_gifts', to='secretsanta.Gift'),
        ),
    ]
