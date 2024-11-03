from django.db import models


class Tenant(models.Model):
    name = models.CharField(max_length=64, unique=True, null=False, blank=False)

    def __str__(self):
        return self.name
