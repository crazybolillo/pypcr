from datetime import datetime, timedelta
from json import loads
from pathlib import Path

from django.test import TestCase

from registry.models.endpoint import Endpoint
from registry.models.identity import Identity
from registry.models.template import Template
from registry.models.tenant import Tenant
from registry.models.token import Token


class TestViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        with open(Path(__file__).parent / "data" / "json-template.j2") as fd:
            content = fd.read()

        cls.tenant = Tenant.objects.create(name="frutsi")
        cls.endpoint = Endpoint.objects.create(
            username="kiwi",
            password="kiwipassword",
            display_name="Mr. Kiwi",
            tenant=cls.tenant,
        )
        cls.tmpl = Template.objects.create(
            tenant=cls.tenant,
            name="json.txt",
            mime="application/json",
            content=content,
        )
        cls.identity = Identity.objects.create(
            model="J139",
            mac="123456789012",
            endpoint=cls.endpoint,
        )
        cls.valid_ua = (
            "Mozilla/4.0 (compatible; MSIE 6.0) AVAYA/J139-4.1.5.0.6 (MAC:123456789012)"
        )

    def _validate_response_with_endpoint(self, res):
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers["Content-Type"], self.tmpl.mime)

        body = loads(res.content)
        self.assertEqual(body["username"], self.endpoint.username)
        self.assertEqual(body["password"], self.endpoint.password)
        self.assertEqual(body["display_name"], self.endpoint.display_name)
        self.assertEqual(body["sip_server"], "sip.example.com")
        self.assertEqual(body["sip_protocol"], "tcp")

    def test_token_valid(self):
        token = Token.objects.create(
            endpoint=self.endpoint,
            template=self.tmpl,
            expires=datetime.now() + timedelta(hours=1),
        )

        res = self.client.get(f"/token/{token.key}")
        self._validate_response_with_endpoint(res)

    def test_token_invalid(self):
        res = self.client.get("/token/random-crap-key")
        self.assertEqual(res.status_code, 404)

    def test_token_expired(self):
        token = Token.objects.create(
            endpoint=self.endpoint,
            template=self.tmpl,
            expires=datetime.now() - timedelta(hours=1),
        )
        res = self.client.get(f"/token/{token.key}")

        self.assertEqual(res.status_code, 401)

    def test_file_valid_all(self):
        res = self.client.get(
            f"/{self.tenant.name}/{self.tmpl.name}",
            headers={
                "User-Agent": self.valid_ua,
            },
        )
        self._validate_response_with_endpoint(res)

    def test_file_invalid_name(self):
        res = self.client.get(
            f"/{self.tenant.name}/somerando",
            headers={
                "User-Agent": self.valid_ua,
            },
        )
        self.assertEqual(res.status_code, 404)

    def test_file_invalid_ua(self):
        res = self.client.get(
            f"/{self.tenant.name}/{self.tmpl.name}",
            headers={"User-Agent": "invalid-ua"},
        )
        body = loads(res.content)

        self.assertEqual(res.status_code, 200)

        self.assertEqual(body["sip_server"], "sip.example.com")
        self.assertEqual(body["sip_protocol"], "tcp")

        self.assertFalse("username" in body)
        self.assertFalse("password" in body)
        self.assertFalse("display_name" in body)
