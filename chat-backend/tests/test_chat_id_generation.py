from django.test import TestCase
from chatnoir_chat.models import Chat
from chatnoir_chat.chat_messages import chat_id_or_none

def mock_request(user):
    class MockedRequest():
        def __init__(self):
            self.headers = {'X-Disraptor-User': user, 'X-Disraptor-App-Secret-Key': 'no-secret-key'}
            self.method = 'POST'
            self.POST = {'message': 'Message', 'endpoint': 'endpoint'}
    return MockedRequest()

class TestChatIdGeneration(TestCase):
    def setUp(self):
        Chat.objects.all().delete()
        Chat.objects.create(chat_id = 'chat_id_1', user_id = 'user_id_1')
        Chat.objects.create(chat_id = 'chat_id_2', user_id = 'user_id_2')
    
    def test_wrong_chat(self):
        request = mock_request('new-user')
        chat_id = chat_id_or_none(request, 'chat_id_1')

        self.assertNotEquals(chat_id, 'chat_id_1')
        self.assertNotEquals(chat_id, 'chat_id_2')

        for i in range(10):
            self.assertEquals(chat_id, chat_id_or_none(request, chat_id))

    def test_correct_chat_user_01(self):
        request = mock_request('user_id_1')
        chat_id = chat_id_or_none(request, 'chat_id_1')

        self.assertEquals(chat_id, 'chat_id_1')
        self.assertNotEquals(chat_id, 'chat_id_2')

    def test_correct_chat_user_02(self):
        request = mock_request('user_id_2')
        chat_id = chat_id_or_none(request, 'chat_id_2')

        self.assertEquals(chat_id, 'chat_id_2')
        self.assertNotEquals(chat_id, 'chat_id_1')

    def tearDown(self) -> None:
        Chat.objects.all().delete()