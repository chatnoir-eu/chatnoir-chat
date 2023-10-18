from chatnoir_chat.models import RequestAndResponseCache
from django.conf import settings
from django.http import HttpRequest, HttpResponseForbidden, JsonResponse
import hashlib
from discourse_client_in_disraptor import request_is_in_group, check_disraptor_token, get_disraptor_user
from django.http import HttpResponseNotAllowed
from chatnoir_chat.custom_backends import run_custom_endpoint
import json


def return_response_from_cache_or_none(endpoint: str, user_id:str, request: str, seed: str):
    """
    Returns the response from the cache if there is already a request for this endpoint by this user for the request and the seed.
    Otherwise returns None.

    :param endpoint: The endpoint of the request.
    :param user_id: The user id.
    :param request: The request text.
    :param seed: The seed of the request.
    :return: The response from the cache if the request is already in the cache or None.
    """
    ret = RequestAndResponseCache.objects.filter(user_id = user_id, md5_hash_of_request = md5_hash(request), request_text = request, seed = seed, endpoint = endpoint)

    if len(ret) > 0:
        return ret[0].response_text

    return None

def seq2seq(request: HttpRequest, endpoint):
    """
    Returns the response for the request while using caching if possible

    :param request: The http request. Must contain the user_id, the text_request, and the seed.
    :param endpoint: The endpoint of the request.
    :return: The response.
    """
    if request.method != 'POST':
        return HttpResponseNotAllowed('Only HTTP POST is allowed.')
    user_id = get_disraptor_user(request, allow_unauthenticated_user=True)
    request_body = json.loads(request.body.decode('utf-8'))
    text_request = request_body['text_request']
    seed = request_body.get('seed', 'no-seed')

    return return_response(request, endpoint, user_id, text_request, seed)

@check_disraptor_token
def return_response(request: HttpRequest, endpoint: str, user_id:str, text_request: str, seed: str):
    """
    Returns the response for the request while using caching if possible

    :param request: The http request.
    :param endpoint: The endpoint of the request.
    :param user_id: The user id.
    :param text_request: The request text.
    :param seed: The seed of the request.
    :return: The response.
    """
    if not endpoint.startswith('custom-backend-') and endpoint not in settings.PUBLIC_CHAT_ENDPOINTS and not request_is_in_group(request=request, group=endpoint, app='chatnoir_chat'):
        return HttpResponseForbidden(f'Forbidden to access "{endpoint}"')

    ret = return_response_from_cache_or_none(endpoint, user_id, text_request, seed)
    if ret is None:
        if endpoint.startswith('custom-backend-'):
            ret = run_custom_endpoint(endpoint, text_request)
        else:
            ret = settings.STATIC_CHAT_ENDPOINTS[endpoint](text_request)

        insert_entry_to_cache(endpoint, user_id, text_request, seed, ret)

    return JsonResponse({'request': text_request, 'response': ret})

def insert_entry_to_cache(endpoint: str, user_id:str, request: str, seed: str, response: str):
    """
    Inserts an entry to the cache.

    :param endpoint: The endpoint of the request.
    :param user_id: The user id.
    :param request: The request text.
    :param seed: The seed of the request.
    :param response: The response.
    :return: None.
    """
    RequestAndResponseCache.objects.create(user_id = user_id,
                                           md5_hash_of_request = md5_hash(request), seed = seed, request_text = request, response_text = response,
                                           endpoint = endpoint)

def md5_hash(request):
    """
    Returns the md5 hash of the request.
    """
    return hashlib.md5(request.encode('utf-8')).hexdigest()
