from django.db import models
from secrets import token_urlsafe

from registry.models.endpoint import Endpoint
from registry.models.template import Template


def _generate_token():
    return token_urlsafe(32)


class Token(models.Model):
    key = models.CharField(
        max_length=255, unique=True, null=False, blank=False, default=_generate_token
    )
    endpoint: Endpoint = models.ForeignKey(
        Endpoint, on_delete=models.CASCADE, null=False
    )
    template: Template = models.ForeignKey(
        Template, on_delete=models.CASCADE, null=False
    )
    expires = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return f"{self.endpoint.username} ({self.template.name})"
