from django.test import TestCase
from chatnoir_chat.chat_cache import return_response_from_cache_or_none


class TestIfEntriesAreInCache(TestCase):
    def test_for_echo_endpoint(self):
        actual = return_response_from_cache_or_none(endpoint = 'echo', user_id = '', request = 'hello', seed = '1')
        self.assertIsNone(actual)

    def test_for_return_count_endpoint(self):
        actual = return_response_from_cache_or_none(endpoint = 'return_count', user_id = '', request = 'hello', seed = '1')
        self.assertIsNone(actual)