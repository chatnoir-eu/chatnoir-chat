from django.test import TestCase
from chatnoir_chat.models import Chat, ChatMessage
from chatnoir_chat.chat_messages import send_new_chat_message, load_chat, chat_history, load_chat_models
import json

def mock_request(user, message):
    class MockedRequest():
        def __init__(self):
            self.headers = {'X-Disraptor-User': user, 'X-Disraptor-Groups': 'chatnoir_chat___echo', 'X-Disraptor-App-Secret-Key': 'no-secret-key'}
            self.method = 'POST'
            self.body = ('{"message": "' + message + '", "endpoint": "echo"}').encode('utf-8')
    return MockedRequest()

class TestChatMessages(TestCase):
    def setUp(self):
        ChatMessage.objects.all().delete()
        Chat.objects.all().delete()

    def test_chat_for_single_message(self):
        request = mock_request('new-user', 'm1')
        response = send_new_chat_message(request, 'does-not-exist')

        self.assertEquals(response.status_code, 200)
        response = json.loads(response.content.decode('utf-8'))
        del response['chat_id']
        del response['id']
        response = json.dumps(response)

        self.assertEquals(response, '{"text": "m1", "type": "bot", "endpoint": "echo"}')

    def test_loading_chat_for_single_message(self):
        request = mock_request('new-user', 'm1')
        response = send_new_chat_message(request, 'does-not-exist')

        self.assertEquals(response.status_code, 200)
        response = json.loads(response.content.decode('utf-8'))
        chat_id = response['chat_id']

        actual = load_chat(request, chat_id)
        actual = json.loads(actual.content.decode('utf-8'))
        for i in actual['messages']:
            del i['id']
            del i['chat_id']
        del actual['chat_id']
        self.assertEquals(actual, {'messages': [{'text': 'm1', 'type': 'user', 'endpoint': 'echo'}, {'text': 'm1', 'type': 'bot', 'endpoint': 'echo'}], 'selectedChatModel': 'echo'})

    def test_empty_chat_history_new_user(self):
        request = mock_request('new-user', 'm1')
        response = chat_history(request)

        self.assertEquals(response.status_code, 200)
        response = json.loads(response.content.decode('utf-8'))
        titles = [i['title'] for i in response['chatHistory']]
        self.assertEquals(titles, [])

    def test_non_empty_chat_history(self):
        request = mock_request('u1', 'm1')
        response = send_new_chat_message(request, 'c1')
        response = send_new_chat_message(request, 'c2')
        response = chat_history(request)

        self.assertEquals(response.status_code, 200)
        response = json.loads(response.content.decode('utf-8'))
        titles = [i['title'] for i in response['chatHistory']]
        self.assertEquals(titles, ['Unnamed Chat', 'Unnamed Chat'])

    def test_load_chat_models(self):
        request = mock_request('u1', 'm1')
        response = load_chat_models(request)
        response = response.content.decode('utf-8')

        self.assertEquals(response, '''{"chatModels": [{"id": "alpaca-en-7b", "title": "alpaca-en-7b"}, {"id": "gpt2-xl", "title": "gpt2-xl"}, {"id": "echo", "title": "echo"}, {"id": "return_count", "title": "return_count"}]}''')

    def tearDown(self):
        ChatMessage.objects.all().delete()
        Chat.objects.all().delete()
