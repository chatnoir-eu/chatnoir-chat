from django.test import TestCase
from chatnoir_chat.chat_cache import return_response_from_cache_or_none, return_response

def mock_request(groups):
    class MockedRequest():
        def __init__(self):
            self.headers = {'X-Disraptor-Groups': ','.join(['chatnoir_chat___' + i for i in groups]), 'X-Disraptor-App-Secret-Key': 'no-secret-key'}
    return MockedRequest()

class TestReturn405ResponseIfNotAuthenticated(TestCase):
    def test_user_without_group_gets_405(self):
        request = mock_request(groups=[])
        
        actual = return_response(request, endpoint = 'echo', user_id = 'u1', text_request = 'u1', seed = '1')
        self.assertEqual(403, actual.status_code)

    def test_user_with_wrong_group_gets_405(self):
        request = mock_request(groups=['some-endpoint'])
        
        actual = return_response(request, endpoint = 'echo', user_id = 'u1', text_request = 'u1', seed = '1')
        self.assertEqual(403, actual.status_code)

    def test_user_with_correct_group_gets_200(self):
        request = mock_request(groups=['echo'])
        
        actual = return_response(request, endpoint = 'echo', user_id = 'u1', text_request = 'u1', seed = '1')
        self.assertEqual(200, actual.status_code)
        self.assertEqual('{"request": "u1", "response": "u1"}', actual.content.decode('utf-8'))
