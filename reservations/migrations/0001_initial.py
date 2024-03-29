# Generated by Django 4.1.5 on 2023-01-06 13:43

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code', models.CharField(editable=False, max_length=6, verbose_name='Code')),
                ('check_in', models.DateField(verbose_name='Check-in')),
                ('check_out', models.DateField(verbose_name='Check-out')),
                ('price', models.DecimalField(decimal_places=2, max_digits=11, verbose_name='Price')),
                ('total_guests', models.PositiveSmallIntegerField(verbose_name='Number of guests')),
                ('comments', models.TextField(blank=True, default='', verbose_name='Comments')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('listing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='listings.listing', verbose_name='Listing')),
            ],
            options={
                'verbose_name': 'Reservation',
                'verbose_name_plural': 'Reservations',
            },
        ),
    ]
