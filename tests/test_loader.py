from unittest import TestCase
from datetime import datetime

from cmku_client.lib.loader import Loader

ACTIONS_TEST_DATA = [
    {
        "id": 12,
        "name": "Test action name 12",
        "start": "2020-06-06T00:00:00",
        "end": "2020-06-06T00:00:00",
    },
    {
        "id": 13,
        "name": "Test keyword name 12",
        "start": "2020-06-06T00:00:00",
        "end": "2020-07-06T00:00:00",
    },
    {
        "id": 14,
        "name": "Test keyword name 13",
        "start": "2020-06-06T00:00:00",
        "end": "2020-08-06T00:00:00"
    }
]


class TestLoader(Loader):
    def _get(self):
        return ACTIONS_TEST_DATA


class LoaderTestCase(TestCase):
    def setUp(self):
        self._loader = TestLoader()

    def test_date_search(self):
        result = self._loader.load_actions_by_date(date_from=datetime(2020, 6, 6), date_to=datetime(2020, 7, 6))
        assert len(result) == 2
        result = self._loader.load_actions_by_date(date_from=datetime(2020, 6, 6), date_to=datetime(2020, 6, 6))
        assert len(result) == 1

    def test_name_search(self):
        result = self._loader.load_actions_by_name("12")
        assert len(result) == 2

    def test_load(self):
        result = self._loader.load_actions()
        assert len(result) == 3