# Generated by Django 4.0.10 on 2025-06-16 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='comment',
            name='discussions_parent__8dd19d_idx',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='parent',
        ),
        migrations.AddField(
            model_name='comment',
            name='children',
            field=models.ManyToManyField(to='discussions.comment'),
        ),
    ]
