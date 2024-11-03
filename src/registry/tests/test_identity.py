from dataclasses import dataclass
from unittest import TestCase

from registry.models.identity import Identity


@dataclass
class MatchCase:
    name: str
    ua: str
    want: Identity


@dataclass
class NoMatchCase:
    name: str
    ua: str


class TestIdentity(TestCase):
    def test_identify_matches(self):
        cases = [
            MatchCase(
                name="j139",
                ua="Mozilla/4.0 (compatible; MSIE 6.0) AVAYA/J139-4.1.5.0.6 (MAC:c81f4aef9689)",
                want=Identity(model="J139", mac="c81f4aef9689"),
            ),
            MatchCase(
                name="j159",
                ua="Mozilla/4.0 (compatible; MSIE 6.0) AVAYA/J159-4.1.0 (MAC:c41f3aef9689)",
                want=Identity(model="J159", mac="c41f3aef9689"),
            ),
            MatchCase(
                name="j179",
                ua="Mozilla/4.0 (compatible; MSIE 6.0) AVAYA/J179-4.2.0 (MAC:c41f3ae55689)",
                want=Identity(model="J179", mac="c41f3ae55689"),
            ),
        ]

        for case in cases:
            with self.subTest(case.name, case=case):
                res = Identity.objects.identify(case.ua)
                self.assertTrue(res, "No match found")
                self.assertEqual(res.mac, case.want.mac)
                self.assertEqual(res.model, case.want.model)

    def test_identify_not_matches(self):
        cases = [
            NoMatchCase(
                name="jseries-wrong-model",
                ua="Mozilla/4.0 (compatible; MSIE 6.0) AVAYA/R134-4.2.0 (MAC:c41f3ae55689)",
            ),
        ]

        for case in cases:
            with self.subTest(case.name, case=case):
                res = Identity.objects.identify(case.ua)
                self.assertFalse(res, "Match should not be found")
