from django.test import TestCase
from chatnoir_chat.chat_cache import return_response
import json

def mock_request(groups):
    class MockedRequest():
        def __init__(self):
            self.headers = {'X-Disraptor-Groups': ','.join(['chatnoir_chat___' + i for i in groups]), 'X-Disraptor-App-Secret-Key': 'no-secret-key'}
    return MockedRequest()

class TestCacheForCountEndpoint(TestCase):
    def test_cache_for_same_users(self):
        for i in range(10):
            actual = return_response(request=mock_request(['return_count']), endpoint = 'return_count', user_id = 'u1', text_request = 'u1', seed = '1')
            self.assertEquals('u11', json.loads(actual.content.decode('utf-8'))['response'])

    def test_no_cache_for_different_users(self):
        for i in range(10):
            actual = return_response(request=mock_request(['return_count']), endpoint = 'return_count', user_id = 'user-' + str(i), text_request = 'tttt-', seed = '1')
            self.assertEquals('tttt-'+ str(i+1), json.loads(actual.content.decode('utf-8'))['response'])