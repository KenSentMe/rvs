# Generated by Django 4.2.11 on 2024-05-28 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uitspraken', '0008_uitspraak_beslissing_alter_uitspraak_label'),
    ]

    operations = [
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('letter', models.CharField(max_length=1)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='uitspraak',
            name='letters',
            field=models.ManyToManyField(to='uitspraken.letter'),
        ),
    ]
