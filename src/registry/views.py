from datetime import datetime
from http import HTTPStatus

from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_http_methods

from .models.identity import Identity
from .models.template import Template
from .models.token import Token


@require_http_methods(["GET"])
def token(_request, key):
    try:
        entry = Token.objects.get(key=key)
    except Token.DoesNotExist:
        return HttpResponseNotFound()

    now = datetime.now()
    if now > entry.expires:
        return HttpResponse(status=HTTPStatus.UNAUTHORIZED)

    return HttpResponse(
        entry.template.render({"endpoint": entry.endpoint}),
        content_type=entry.template.mime,
    )


@require_http_methods(["GET"])
def file(request, tenant, filename):
    try:
        tmpl = Template.objects.get(name=filename, tenant__name=tenant)
    except Template.DoesNotExist:
        return HttpResponseNotFound()

    ua = request.META["HTTP_USER_AGENT"]
    identity = Identity.objects.identify(ua)
    if not identity:
        return HttpResponse(
            tmpl.render(),
            content_type=tmpl.mime,
        )

    identity = Identity.objects.get(model=identity.model, mac=identity.mac)
    if not identity:
        return HttpResponse(
            tmpl.render(),
            content_type=tmpl.mime,
        )

    return HttpResponse(
        tmpl.render({"endpoint": identity.endpoint}),
        content_type=tmpl.mime,
    )
