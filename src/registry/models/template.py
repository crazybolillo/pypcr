from django.db import models

from registry.models.tenant import Tenant
from django.template import Template as JinjaTmpl, Context


class Template(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    mime = models.CharField(max_length=64, null=False, blank=False)
    content = models.TextField(null=False, blank=False)

    constraints = [
        models.UniqueConstraint(fields=["name", "tenant"], name="unique_name_tenant"),
    ]

    def __str__(self):
        return self.name

    def render(self, values: dict | None = None):
        jinja = JinjaTmpl(self.content)
        if values:
            ctx = Context(values)
        else:
            ctx = Context()

        return jinja.render(ctx)
