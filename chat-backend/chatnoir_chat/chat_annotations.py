from chatnoir_chat.chat_messages import chat_id_or_none
from django.http import HttpRequest, HttpResponseNotAllowed, JsonResponse

# Adopted from https://arxiv.org/pdf/2311.04694.pdf
GIENAPP_CONVERSATION_ANNOTATIONS = [
    {'question_id': '1', 'question_text': 'Are the responses well structured? (Logical Coherence of 1 if there are badly structured responses, 5 if all responses are well structured)', 'response_type': 'Likert'},
    {'question_id': '2', 'question_text': 'Do all responses have a uniform style of speech? (Stylistic Coherence)', 'response_type': 'Yes/No'},
    {'question_id': '3', 'question_text': 'Do the responses cover diverse information? (Broad Coverage of 1 for missing broadness, 5 for broad coverage)', 'response_type': 'Likert'},
    {'question_id': '4', 'question_text': 'Do the responses offer detailed information? (Deep Coverage of 1 if no details, 5 for deep details)', 'response_type': 'Likert'},
    {'question_id': '5', 'question_text': 'Are there responses that contradict each other? (Internal Consistency)', 'response_type': 'Yes/No'},
    {'question_id': '6', 'question_text': 'Are external sources accurately cited and referenced? (External Consistency)', 'response_type': 'Yes/No'},
    {'question_id': '7', 'question_text': 'Are the statements verifiably true? (Factual Correctness)', 'response_type': 'Yes/No'},
    {'question_id': '8', 'question_text': 'Are the responses within the scope of the information need? (Topical Correctness)', 'response_type': 'Yes/No'},
    {'question_id': '9', 'question_text': 'Are the responses written in an easily readable way? (Language Clarity)', 'response_type': 'Yes/No'},
    {'question_id': '10', 'question_text': 'Do the responses focus on the most salient points? (Content Clarity).', 'response_type': 'Yes/No'},
]

GIENAPP_UTTERANCE_ANNOTATIONS = {'utterance_id': '1', 'questions': [
    {'question_id': '1', 'question_text': 'Is the response structured well? (Logical Coherence)', 'response_type': 'Yes/No'},
    {'question_id': '2', 'question_text': 'Does the response have a uniform style of speech? (Stylistic Coherence)', 'response_type': 'Yes/No'},
    {'question_id': '3', 'question_text': 'Does the response cover diverse information? (Broad Coverage)', 'response_type': 'Yes/No'},
    {'question_id': '4', 'question_text': 'Does the response offer detailed information? (Deep Coverage)', 'response_type': 'Yes/No'},
    {'question_id': '5', 'question_text': 'Is the response free of contradictions? (Internal Consistency)', 'response_type': 'Yes/No'},
    {'question_id': '6', 'question_text': 'Is the statement conveying from sources accurately? (External Consistency)', 'response_type': 'Yes/No'},
    {'question_id': '7', 'question_text': 'Does the statement state things that are verifiably true? (Factual Correctness)', 'response_type': 'Yes/No'},
    {'question_id': '8', 'question_text': 'Does the statement state things within the scope of the users information need? (Topical Correctness)', 'response_type': 'Yes/No'},
    {'question_id': '9', 'question_text': 'Is a statement written in an easily readable way? (Language Clarity)', 'response_type': 'Yes/No'},
    {'question_id': '10', 'question_text': 'Does the statement put its focus on the most salient points? (Content Clarity).', 'response_type': 'Yes/No'},
]}


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

    return JsonResponse({'conversationAnnotation': GIENAPP_CONVERSATION_ANNOTATIONS, 'utteranceAnnotations': GIENAPP_UTTERANCE_ANNOTATIONS})