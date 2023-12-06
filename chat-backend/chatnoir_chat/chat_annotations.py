from chatnoir_chat.chat_messages import chat_id_or_none
from django.http import HttpRequest, HttpResponseNotAllowed, JsonResponse

EXAM_ANNOTATION = [
    {'question_id': '1', 'question_text': 'How do you feel? (1 bad, 5 good)', 'response_type': 'Likert'},
    {'question_id': '2', 'question_text': 'Do you like the annotation?', 'response_type': 'Yes/No'},
    {'question_id': '3', 'question_text': 'Here some free text', 'response_type': 'Text'},
]

def annotations_for_chat(request: HttpRequest, chat_id: str):
    """
    Returns all annotations for the chat with chat id.

    :param request: The http request. Must contain the user_id.
    :param chat_id: The id of the chat.
    :return: The response.
    """
    chat_id = chat_id_or_none(request, chat_id)

    if not chat_id or type(chat_id) != str:
        return HttpResponseNotAllowed('Not allowed to see / start this chat')

    return JsonResponse({'conversationAnnotation': EXAM_ANNOTATION})