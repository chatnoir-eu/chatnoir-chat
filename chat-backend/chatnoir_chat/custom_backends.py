import threading
import json
import uuid
from django.http import HttpRequest, HttpResponseNotAllowed, JsonResponse
from discourse_client_in_disraptor.discourse_api_client import _DISRAPTOR_UNAUTHENTICATED_GUEST_USER
from discourse_client_in_disraptor import request_is_in_group, check_disraptor_token, get_disraptor_user
from wsgiref.simple_server import make_server
from ws4py.websocket import WebSocket
from ws4py.server.wsgirefserver import WSGIServer, WebSocketWSGIRequestHandler
from ws4py.server.wsgiutils import WebSocketWSGIApplication
from copy import deepcopy
import os
import posix


@check_disraptor_token
def get_custom_backend(request: HttpRequest, backend_id: str):
    from chatnoir_chat.models import CustomBackends
    user_id = get_disraptor_user(request, allow_unauthenticated_user=True)

    if backend_id:
        ret = CustomBackends.objects.filter(backend_id = backend_id)
        if ret and len(ret) > 0 and (ret[0].user_id == user_id or ret[0].user_id == _DISRAPTOR_UNAUTHENTICATED_GUEST_USER):
            return ret[0]
    
    return CustomBackends.objects.create(user_id = user_id, backend_id=str(uuid.uuid4()))

def edit_custom_backend(request: HttpRequest):
    request_body = json.loads(request.body.decode('utf-8'))
    backend_id = request_body.get('backend_id')
    display_name = request_body.get('title', 'Unnamed Backend')
    description = request_body.get('description', 'Please add a description.')

    ret = get_custom_backend(request, backend_id)

    if backend_id is not None and (type(ret) == HttpResponseNotAllowed or ret.backend_id != backend_id):
        return HttpResponseNotAllowed('You are not allowed to acces')

    if display_name != None or description != None:
        ret.display_name = display_name
        ret.description = description
        ret.save()

    return JsonResponse({'backend_id': ret.backend_id, 'title': ret.display_name, 'description': ret.description})

def run_custom_endpoint(endpoint, text):
    backend_id = endpoint.replace('custom-backend-', '')
    input_pipe = f'/tmp/{backend_id}-input'
    id = str(uuid.uuid4())

    with open(input_pipe, "w") as inp:
        inp.write(json.dumps({'text': text, 'uuid': id}) +'\n')

    for i in range(200):
        import time
        time.sleep(.05)
        if os.path.isfile('/tmp/' + id):
            with open('/tmp/' + id, "r") as outp:
                ret = json.load(outp)['text']
            delete_file_failsave('/tmp/' + id)
            
            return ret
    
    raise ValueError('Can not read the response: "/tmp/' + id + '".')

def delete_file_failsave(file):
    try:
        os.remove(file)
    except: pass

class ChatnoirChatCustomBackendWebSocket(WebSocket):
    def opened(self):
        self.pending_uuid = None
        self.thread = None
        return super().opened()

    def received_message(self, message):
        message = deepcopy(json.loads(str(message)))
        ws = self

        if not self.pending_uuid and 'backend_id' in message and message['backend_id'] and '/' not in message['backend_id'] and not self.thread:
            input_pipe = f'/tmp/{message["backend_id"]}-input'
            
            def foo():
                while True:
                    delete_file_failsave(input_pipe)
                    posix.mkfifo(input_pipe)
                    try:
                        with open(input_pipe, "r") as inp:
                            if ws.pending_uuid != None:
                                self.close(self, code=1000, reason='Unexpected message.')
                                raise ValueError('dsaadsdsa')

                            l = json.load(inp)
                            ws.pending_uuid = l['uuid']
                            l = l['text']
                    except:
                        continue

                    if not l:
                        continue

                    ws.send(json.dumps({'uuid':ws.pending_uuid, 'text': l}))

            self.thread = threading.Thread(target=foo, name="Websockets", daemon=True)
            self.thread.start()
            return

        if self.pending_uuid and ('uuid' not in message or message['uuid'] != self.pending_uuid):
            self.close(self, code=1000, reason='Unexpected message.')
            raise ValueError('dsaadsdsa')

        with open('/tmp/' + message['uuid'], 'w') as f:
            f.write(json.dumps(message))
        
        ws.pending_uuid = None  

def __run_websocket_server():
    server = make_server('', 8888, server_class=WSGIServer,
                     handler_class=WebSocketWSGIRequestHandler,
                     app=WebSocketWSGIApplication(handler_cls=ChatnoirChatCustomBackendWebSocket))
    server.initialize_websockets_manager()
    server.serve_forever()

def websocket_server_in_background():
    websocket_thread = threading.Thread(target=__run_websocket_server, name="Websockets", daemon=True)
    websocket_thread.start()
