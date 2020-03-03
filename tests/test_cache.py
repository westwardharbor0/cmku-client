from unittest import TestCase

from cmku_client.lib.cache import Cacher


class CacherTestCase(TestCase):
    @staticmethod
    def test_disabled():
        params, result = ("test_case", 1),  (1, 2, 3)
        cacher = Cacher()
        cacher._store_cache(params, result)
        cached = cacher._check_cache(params)
        print(cached)
        assert cached is None

    @staticmethod
    def test_store():
        params, result = ("test_case", 1), (1, 2, 3)
        cacher = Cacher(cache=True)
        cacher._store_cache(params, result)
        cached = cacher._check_cache(params)
        assert cached == result
