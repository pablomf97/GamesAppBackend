# Generated by Django 3.2 on 2021-04-17 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamesapp', '0004_alter_listgame_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listgame',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
