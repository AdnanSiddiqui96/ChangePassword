# Generated by Django 4.2.7 on 2023-11-21 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='whitelistToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(default='', max_length=255)),
                ('user_agent', models.TextField(default='')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('role_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.account')),
            ],
        ),
    ]