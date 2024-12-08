# Generated by Django 4.2.3 on 2024-11-11 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0003_rename_answer_id_answers_answers_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='test_type',
            field=models.CharField(choices=[('STROOP1', 'stroop1'), ('STROOP2', 'stroop2'), ('STROOP3', 'stroop3'), ('STROOP4', 'stroop4'), ('ARITHM', 'arithm'), ('SPATIAL', 'spatial'), ('SHAPES', 'shapes'), ('COLOR', 'color'), ('SHAPES_COLOR', 'shapes_color'), ('SHAPES_SPATIAL', 'shapes_spatial'), ('MEMORY', 'memory'), ('MUNSTER', 'munster'), ('RAVEN', 'raven')], max_length=255),
        ),
    ]
