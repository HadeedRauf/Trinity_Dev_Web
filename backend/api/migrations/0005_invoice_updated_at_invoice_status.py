# Generated migration to add missing invoice fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_populate_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='status',
            field=models.CharField(
                blank=True,
                max_length=20,
                choices=[
                    ('pending', 'Pending'),
                    ('completed', 'Completed'),
                    ('cancelled', 'Cancelled'),
                ],
                default='completed'
            ),
        ),
    ]
