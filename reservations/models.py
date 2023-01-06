import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Reservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(_('Code'), max_length=6, editable=False)
    check_in = models.DateField(_('Check-in'))
    check_out = models.DateField(_('Check-out'))
    price = models.DecimalField(_('Price'), max_digits=11, decimal_places=2)
    total_guests = models.PositiveSmallIntegerField(_('Number of guests'))
    comments = models.TextField(_('Comments'), blank=True, default='')
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    listing = models.ForeignKey(
        'listings.Listing', on_delete=models.SET_NULL, null=True,
        verbose_name=_('Listing'))

    class Meta:
        verbose_name = _('Reservation')
        verbose_name_plural = _('Reservations')
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.code = uuid.uuid4().hex[:6].upper()
        super().save(*args, **kwargs)
