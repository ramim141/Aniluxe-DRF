# Generated by Django 5.0.4 on 2024-09-06 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_review_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
