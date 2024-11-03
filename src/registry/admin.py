from django.contrib import admin

from registry.models.endpoint import Endpoint
from registry.models.identity import Identity
from registry.models.template import Template
from registry.models.tenant import Tenant
from registry.models.token import Token


class TenantAdmin(admin.ModelAdmin):
    list_display = ["name"]


class EndpointAdmin(admin.ModelAdmin):
    list_display = ["username", "tenant"]


class TemplateAdmin(admin.ModelAdmin):
    list_display = ["name", "mime", "tenant"]


class TokenAdmin(admin.ModelAdmin):
    list_display = ["endpoint", "template", "expires"]
    readonly_fields = ["key"]


admin.site.register(Tenant, TenantAdmin)
admin.site.register(Endpoint, EndpointAdmin)
admin.site.register(Identity)
admin.site.register(Template, TemplateAdmin)
admin.site.register(Token, TokenAdmin)
