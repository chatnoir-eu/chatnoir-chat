from django.test import TestCase
from chatnoir_chat.models import CustomBackends, ChatMessage, Chat
from chatnoir_chat.custom_backends import edit_custom_backend
from chatnoir_chat.chat_messages import chat_id_or_none, send_new_chat_message
import threading
import json
import time
"""
from websocket import create_connection
ws = create_connection("ws://localhost:8888/ws/chat/foo")
print("Sending 'Hello, World'...")
ws.send("Hello, World")
print("Sent")
print("Receiving...")
result =  ws.recv()
print("Received '%s'" % result)
ws.close()
"""
def serve_chat_backend(backend_id, backend_implementation, in_backend_thread=False):
    if in_backend_thread:
        thread_method = lambda: serve_chat_backend(backend_id, backend_implementation)
        threading.Thread(target=thread_method, name="serve_chat_backend_thread", daemon=True).start()
        time.sleep(.05)
        return

    from websocket import create_connection
    ws = create_connection(f"ws://localhost:8888/ws/chat/{backend_id}")
    ws.send(json.dumps({'backend_id': backend_id}))
    while True:
        result = json.loads(ws.recv())
        ret = backend_implementation(result['text'])
        ws.send(json.dumps({'uuid': result['uuid'], 'text': ret, 'backend_id': backend_id}))

def mock_request(body, user=None, secret_key='no-secret-key'):
    headers = {'X-Disraptor-App-Secret-Key': secret_key}

    if user:
        headers['X-Disraptor-User'] = user

    class MockedRequest():
        def __init__(self):
            self.headers = headers
            self.method = 'POST'
            self.body = body.encode('utf-8')
    return MockedRequest()

class TestWebSocket(TestCase):
    def setUp(self):
        CustomBackends.objects.all().delete()
        ChatMessage.objects.all().delete()
        Chat.objects.all().delete()
        CustomBackends.objects.create(user_id = 'user-1', backend_id='b1')
        CustomBackends.objects.create(user_id = 'user-2', backend_id='b2')

    def test_wrong_backend_01(self):
        request = mock_request('{"backend_id": "b1"}')
        actual = edit_custom_backend(request)
        self.assertEqual(405, actual.status_code)

    def test_wrong_backend_02(self):
        request = mock_request('{"backend_id": "b1"}', 'user-2')
        actual = edit_custom_backend(request)
        self.assertEqual(405, actual.status_code)

    def test_wrong_backend_03(self):
        request = mock_request('{"backend_id": "b1"}', 'user-1', 'wrong-key')
        actual = edit_custom_backend(request)
        self.assertEqual(405, actual.status_code)

    def test_loading_existing_backend(self):
        request = mock_request('{"backend_id": "b1"}', 'user-1')
        actual = edit_custom_backend(request)
        self.assertEqual(200, actual.status_code)
        actual = json.loads(actual.content.decode('utf-8'))

        self.assertEquals({"backend_id": "b1", "title": "Unnamed Backend", "description": "Please add a description."}, actual)

    def test_modification_of_existing_backend(self):
        request = mock_request('{}')
        actual = edit_custom_backend(request)
        self.assertEqual(200, actual.status_code)
        actual = json.loads(actual.content.decode('utf-8'))
        backend_id = actual['backend_id']

        self.assertEquals({"backend_id": backend_id, "title": "Unnamed Backend", "description": "Please add a description."}, actual)

        request = mock_request('{"backend_id": "' + backend_id + '", "title": "my title", "description": "my description"}')

        actual = edit_custom_backend(request)
        self.assertEqual(200, actual.status_code)
        actual = json.loads(actual.content.decode('utf-8'))

        self.assertEquals({"backend_id": backend_id, "title": "my title", "description": "my description"}, actual)

    def test_websocket_protocoll_01(self):
        request = mock_request('{}')
        chat_id = chat_id_or_none(request, 'does-not-exist')
        self.assertTrue(chat_id and type(chat_id) == str)

        actual = edit_custom_backend(request)
        self.assertEqual(200, actual.status_code)
        backend_id = json.loads(actual.content.decode('utf-8'))['backend_id']

        serve_chat_backend(backend_id, lambda i: 'You said ' + i, True)

        request = mock_request('{"message": "foo bar", "endpoint": "custom-backend-' + backend_id + '"}')
        response = send_new_chat_message(request, chat_id)

        self.assertEquals(response.status_code, 200)
        response = json.loads(response.content.decode('utf-8'))['text']

        self.assertEquals('You said foo bar', response)

    def test_websocket_protocoll_over_multiple_messages(self):
        request = mock_request('{}')
        chat_id = chat_id_or_none(request, 'does-not-exist')
        self.assertTrue(chat_id and type(chat_id) == str)

        actual = edit_custom_backend(request)
        self.assertEqual(200, actual.status_code)
        backend_id = json.loads(actual.content.decode('utf-8'))['backend_id']

        serve_chat_backend(backend_id, lambda i: 'Here we go: ' + i, True)

        request = mock_request('{"message": "1", "endpoint": "custom-backend-' + backend_id + '"}')
        
        response = send_new_chat_message(request, chat_id)
    
        self.assertEquals(response.status_code, 200)
        response = json.loads(response.content.decode('utf-8'))['text']

        self.assertEquals('Here we go: 1', response)
        
        request = mock_request('{"message": "2", "endpoint": "custom-backend-' + backend_id + '"}')
        response = send_new_chat_message(request, chat_id)

        self.assertEquals(response.status_code, 200)
        response = json.loads(response.content.decode('utf-8'))['text']

        self.assertEquals('Here we go: 2', response)

        request = mock_request('{"message": "3", "endpoint": "custom-backend-' + backend_id + '"}')
        response = send_new_chat_message(request, chat_id)

        self.assertEquals(response.status_code, 200)
        response = json.loads(response.content.decode('utf-8'))['text']

        self.assertEquals('Here we go: 3', response)


    def test_websocket_protocoll_over_multiple_messages_in_loop(self):
        request = mock_request('{}')
        chat_id = chat_id_or_none(request, 'does-not-exist')
        self.assertTrue(chat_id and type(chat_id) == str)

        actual = edit_custom_backend(request)
        self.assertEqual(200, actual.status_code)
        backend_id = json.loads(actual.content.decode('utf-8'))['backend_id']

        serve_chat_backend(backend_id, lambda i: 'Alright: ' + i, True)

        for i in range(20):
            request = mock_request('{"message": "' + str(i) + '", "endpoint": "custom-backend-' + backend_id + '"}')
        
            response = send_new_chat_message(request, chat_id)
    
            self.assertEquals(response.status_code, 200)
            response = json.loads(response.content.decode('utf-8'))['text']

            self.assertEquals('Alright: ' + str(i), response)

    def tearDown(self):
        CustomBackends.objects.all().delete()
        ChatMessage.objects.all().delete()
        Chat.objects.all().delete()



"""
from websocket import create_connection
ws = create_connection("wss://chatsocket.web.webis.de/ws/chat/foo")
print("Sending 'Hello, World'...")
ws.send("Hello, World")
print("Sent")
print("Receiving...")
result =  ws.recv()
print("Received '%s'" % result)
ws.close()
"""