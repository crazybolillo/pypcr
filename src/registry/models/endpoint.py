from django.db import models

from registry.models.tenant import Tenant


class Endpoint(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    username = models.CharField(max_length=64, null=False, blank=False)
    password = models.CharField(max_length=128, null=False, blank=False)
    display_name = models.CharField(max_length=128, null=False, blank=False)

    def __str__(self):
        return self.username
