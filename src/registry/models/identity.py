import re

from django.db import models

from registry.models.endpoint import Endpoint


class IdentityManager(models.Manager):
    _avaya_j_regex = re.compile(r"AVAYA/(J\d{3})-(?:\d\.?)+ \(MAC:([abcdef0-9]{12})\)$")

    def _avaya_jseries(self, ua: str) -> "Identity" or None:
        if match := self._avaya_j_regex.search(ua):
            return Identity(model=match.group(1), mac=match.group(2))

    def identify(self, ua: str) -> "Identity" or None:
        for fn in [
            self._avaya_jseries,
        ]:
            identity = fn(ua)
            if identity:
                return identity


class Identity(models.Model):
    class Meta:
        verbose_name_plural = "Identities"

    mac = models.CharField(max_length=12, null=False, blank=False)
    model = models.CharField(max_length=64, null=False, blank=False)
    endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE)

    objects = IdentityManager()
    constraints = [
        models.UniqueConstraint(fields=["mac", "model"], name="unique_mac_model"),
    ]

    def __str__(self):
        return self.mac
