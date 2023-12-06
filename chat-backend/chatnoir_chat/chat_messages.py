from chatnoir_chat.models import Chat, ChatMessage, CustomBackends
from chatnoir_chat.chat_cache import return_response
from discourse_client_in_disraptor import check_disraptor_token, get_disraptor_user
from discourse_client_in_disraptor.discourse_api_client import _DISRAPTOR_UNAUTHENTICATED_GUEST_USER
from django.http import HttpRequest, HttpResponseNotAllowed, JsonResponse
from django.conf import settings
import uuid
import json


@check_disraptor_token
def chat_id_or_none(request: HttpRequest, chat_id: str):
    user_id = get_disraptor_user(request, allow_unauthenticated_user=True)
    ret = Chat.objects.filter(chat_id = chat_id)
    if ret and len(ret) > 0 and (ret[0].user_id == user_id or ret[0].user_id ==_DISRAPTOR_UNAUTHENTICATED_GUEST_USER):
        return ret[0].chat_id

    return Chat.objects.create(user_id = user_id, chat_id=str(uuid.uuid4())).chat_id


def send_new_chat_message(request: HttpRequest, chat_id: str):
    """
    Returns the response for the request while using caching if possible

    :param request: The http request. Must contain the user_id, the endpoint, and the text_request.
    :param chat_id: The id of the chat.
    :return: The response.
    """
    chat_id = chat_id_or_none(request, chat_id)
    user_id = get_disraptor_user(request, allow_unauthenticated_user=True)

    if not chat_id or type(chat_id) != str:
        return HttpResponseNotAllowed('Not allowed to see / start this chat')
    
    request_body = json.loads(request.body.decode('utf-8'))

    endpoint = request_body.get('endpoint')
    message = request_body.get('message')
    response = return_response(request,  endpoint, user_id, message, str(uuid.uuid4()))

    if type(response) != JsonResponse:
        return response
    response = json.loads(response.content.decode('utf-8'))['response']
    
    ChatMessage.objects.create(chat_id=chat_id, text=message, type='user', endpoint=endpoint)
    ret = ChatMessage.objects.create(chat_id=chat_id, text=response, type='bot', endpoint=endpoint)

    return JsonResponse({'id': ret.message_id, 'chat_id': chat_id, 'text': ret.text, 'type': ret.type, 'endpoint': ret.endpoint})

def configure_chat(request: HttpRequest, chat_id: str):
    """
    Configures the settings of the chat.

    :param request: The http request. Must contain the user_id.
    :param chat_id: The id of the chat.
    :return: The response.
    """
    chat_id = chat_id_or_none(request, chat_id)

    if not chat_id or type(chat_id) != str:
        return HttpResponseNotAllowed('Not allowed to see / start this chat')

    request_body = json.loads(request.body.decode('utf-8'))

    chat = Chat.objects.get(chat_id=chat_id)

    if chat.is_finished:
        return HttpResponseNotAllowed('Chat is already finished')

    if 'chat_title' in request_body:
        chat.display_name = request_body['chat_title']
    
    if 'chat_description' in request_body:
        chat.description = request_body['chat_description']

    if 'is_finished' in request_body and request_body['is_finished']:
        chat.is_finished = True

    if 'annotation_dataset' in request_body:
        chat.annotation_dataset = request_body['annotation_dataset']

    if 'annotation_topic' in request_body:
        chat.annotation_topic = request_body['annotation_topic']

    chat.save()

    return JsonResponse({})

def load_chat(request: HttpRequest, chat_id: str):
    """
    Returns the complete chat history for the chat_id.

    :param request: The http request. Must contain the user_id.
    :param chat_id: The id of the chat.
    :return: The response.
    """
    chat_id = chat_id_or_none(request, chat_id)

    if not chat_id or type(chat_id) != str:
        return HttpResponseNotAllowed('Not allowed to see / start this chat')
    
    messages = []
    ret = ChatMessage.objects.filter(chat_id=chat_id).order_by('message_id')
    for i in ret:
        messages += [{'id': i.message_id, 'text': i.text, 'type': i.type, 'endpoint': i.endpoint, 'chat_id': i.chat_id}]

    chat = Chat.objects.get(chat_id=chat_id)

    ret = {'messages': messages, 'chat_id': chat_id, "chat_title": chat.display_name, "chat_description": chat.description,
           'chat_is_finished': chat.is_finished, 'topic_dataset': chat.annotation_dataset, 'topic_topic': chat.annotation_topic,
           'annotation_dataset': chat.annotation_dataset, 'annotation_topic': chat.annotation_topic,
           'specify_topic': chat.annotation_dataset is not None and chat.annotation_topic is not None
          }
    if len(messages) > 0:
        ret['selectedChatModel'] = messages[-1]['endpoint']

    return JsonResponse(ret)

def chat_history(request: HttpRequest):
    """
    Returns all chats of a user.

    :param request: The http request. Must contain the user_id.
    :return: The response.
    """
    user_id = get_disraptor_user(request, allow_unauthenticated_user=True)
    ret = []

    if user_id and user_id != _DISRAPTOR_UNAUTHENTICATED_GUEST_USER:
        ret = Chat.objects.filter(user_id=user_id).order_by('chat_id')
        ret = [{'link': '/cc/' + i.chat_id, 'title': i.display_name} for i in ret]

    return JsonResponse({'chatHistory': ret})

def load_chat_models(request: HttpRequest):
    """
    Returns all chat models available to a user.

    :param request: The http request.
    :return: The response.
    """
    models = [{'id': i, 'title': i} for i in settings.STATIC_CHAT_ENDPOINTS.keys()]
    models += [{'id': 'custom-backend-' + i.backend_id, 'title': i.display_name} for i in CustomBackends.objects.all() if i.display_name != 'Unnamed Backend']

    return JsonResponse({'chatModels': models})