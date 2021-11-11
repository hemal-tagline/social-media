# Generated by Django 3.2.8 on 2021-11-11 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learnings', '0002_author_details_publisher'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='details',
            options={'verbose_name_plural': 'Details'},
        ),
        migrations.AddField(
            model_name='author',
            name='author_pic',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
