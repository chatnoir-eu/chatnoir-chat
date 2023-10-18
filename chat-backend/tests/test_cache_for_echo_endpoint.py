from django.test import TestCase
from chatnoir_chat.chat_cache import return_response_from_cache_or_none, return_response
import json

def mock_request(groups):
    class MockedRequest():
        def __init__(self):
            self.headers = {'X-Disraptor-Groups': ','.join(['chatnoir_chat___' + i for i in groups]), 'X-Disraptor-App-Secret-Key': 'no-secret-key'}
    return MockedRequest()

class TestCacheForEchoEndpoint(TestCase):
    def test_caching_for_message_01_user_01(self):
        expected = 'u1'
        self.assertIsNone(return_response_from_cache_or_none(endpoint = 'echo', user_id = 'u1', request = 'u1', seed = '1'))

        actual = return_response(request=mock_request(['echo']), endpoint = 'echo', user_id = 'u1', text_request = 'u1', seed = '1')
        self.assertEqual(expected, json.loads(actual.content.decode('utf-8'))['response'])

        actual = return_response_from_cache_or_none(endpoint = 'echo', user_id = 'u1', request = 'u1', seed = '1')
        self.assertEqual(expected, actual)

    def test_caching_is_not_observed_over_multiple_users(self):
        request = 'test_caching_is_not_observed_over_multiple_users'
        self.assertIsNone(return_response_from_cache_or_none(endpoint = 'echo', user_id = 'u1', request = request, seed = '1'))

        actual = return_response(endpoint = 'echo', user_id = 'u1', request=mock_request(['echo']), text_request = request, seed = '1')
        self.assertEqual(request, json.loads(actual.content.decode('utf-8'))['response'])

        actual = return_response_from_cache_or_none(endpoint = 'echo', user_id = 'u1', request = request, seed = '1')
        self.assertEqual(request, actual)

        self.assertIsNone(return_response_from_cache_or_none(endpoint = 'echo', user_id = 'u2', request = request, seed = '1'))

        actual = return_response(request=mock_request(['echo']), endpoint = 'echo', user_id = 'u2', text_request = request, seed = '1')
        self.assertEqual(request, json.loads(actual.content.decode('utf-8'))['response'])

        actual = return_response_from_cache_or_none(endpoint = 'echo', user_id = 'u2', request = request, seed = '1')
        self.assertEqual(request, actual)


    def test_caching_is_not_observed_over_multiple_seeds(self):
        request = 'test_caching_is_not_observed_over_multiple_seeds'
        self.assertIsNone(return_response_from_cache_or_none(endpoint = 'echo', user_id = 'u1', request = request, seed = '1'))

        actual = return_response(request=mock_request(['echo']), endpoint = 'echo', user_id = 'u1', text_request = request, seed = '1')
        self.assertEqual(request, json.loads(actual.content.decode('utf-8'))['response'])

        actual = return_response_from_cache_or_none(endpoint = 'echo', user_id = 'u1', request = request, seed = '1')

        self.assertEqual(request, actual)
        request = 'test_caching_is_not_observed_over_multiple_seeds'
        self.assertIsNone(return_response_from_cache_or_none(endpoint = 'echo', user_id = 'u1', request = request, seed = '2'))

        actual = return_response(request=mock_request(['echo']), endpoint = 'echo', user_id = 'u1', text_request = request, seed = '2')
        self.assertEqual(request, json.loads(actual.content.decode('utf-8'))['response'])

        actual = return_response_from_cache_or_none(endpoint = 'echo', user_id = 'u1', request = request, seed = '2')
        self.assertEqual(request, actual)