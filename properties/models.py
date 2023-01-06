import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(_('Name'), max_length=50, unique=True)
    guest_limit = models.PositiveSmallIntegerField(_('Guest limit'))
    bathrooms = models.PositiveSmallIntegerField(_('Bathrooms'))
    accept_pets = models.BooleanField(_('Accept pets'))
    cleaning_price = models.DecimalField(
        _('Cleaning price'), max_digits=11, decimal_places=2)
    activation_date = models.DateField(_('Activation date'), blank=True, null=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Property')
        verbose_name_plural = _('Properties')
        ordering = ['-created_at']

    def __str__(self):
        return self.code
