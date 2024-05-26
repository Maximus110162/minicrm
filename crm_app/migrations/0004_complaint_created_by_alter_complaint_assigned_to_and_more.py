# Generated by Django 4.2.13 on 2024-05-25 06:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0003_alter_complaint_assigned_to_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_complaints', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='assigned_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_complaints', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='client_account',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='client_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='client_phone',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='status',
            field=models.CharField(choices=[('open', 'Открыта'), ('in_progress', 'В работе'), ('closed', 'Закрыта')], default='open', max_length=20),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('operator', 'Оператор'), ('back_office', 'Бэк-офис')], max_length=30),
        ),
    ]
