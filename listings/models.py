import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Listing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform = models.CharField(_('Platform'), max_length=50)
    platform_fee = models.DecimalField(
        _('Platform fee'), max_digits=11, decimal_places=2)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    property = models.ForeignKey(
        'properties.Property', on_delete=models.SET_NULL, null=True,
        verbose_name=_('Property'))

    class Meta:
        verbose_name = _('Listing')
        verbose_name_plural = _('Listings')
        ordering = ['-created_at']

    def __str__(self):
        if not self.property:
            return self.id
        return self.property.code
