# Generated by Django 4.0.10 on 2025-06-17 00:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('discussions', '0002_remove_comment_discussions_parent__8dd19d_idx_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='children',
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='discussions.comment'),
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['parent'], name='discussions_parent__8dd19d_idx'),
        ),
    ]
