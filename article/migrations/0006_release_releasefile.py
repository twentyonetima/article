# Generated by Django 5.0.3 on 2024-04-05 14:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_article_markdown_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('release_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ReleaseFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=255)),
                ('size', models.BigIntegerField()),
                ('upload_date', models.DateTimeField()),
                ('release', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.release')),
            ],
        ),
    ]
