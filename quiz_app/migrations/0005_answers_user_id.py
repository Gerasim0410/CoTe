# Generated by Django 4.2.3 on 2024-11-11 05:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0004_alter_questions_test_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='answers',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
