"""
URL configuration for chatnoir_chat project.
"""
from django.urls import path, re_path
from chatnoir_chat.chat_cache import seq2seq
from chatnoir_chat.ui import veutify_page
from chatnoir_chat.custom_backends import edit_custom_backend
from chatnoir_chat.chat_messages import send_new_chat_message, load_chat, configure_chat, chat_history, load_chat_models
from chatnoir_chat.chat_annotations import annotations_for_chat
from chatnoir_chat.ir_datasets import ir_datasets, topic_description, docs

urlpatterns = [
    path('seq2seq/<str:endpoint>', seq2seq, name='seq2seq'),
    path('load-chat/<str:chat_id>', load_chat, name='load_chat'),
    path('configure-chat/<str:chat_id>', configure_chat, name='configure_chat'),
    path('load-chat-history', chat_history, name='load_chat'),
    path('send-message/<str:chat_id>', send_new_chat_message, name='send_new_chat_message'),
    path('load-chat-models', load_chat_models, name='load_chat_models'),
    path('api/edit-custom-backend', edit_custom_backend, name='edit_custom_backend'),
    path('api/ir-datasets', ir_datasets, name='ir_datasets'),
    path('api/topic_description', topic_description, name='topic_description'),
    path('api/docs', docs, name='docs'),
    path('api/annotations-for-chat/<str:chat_id>', annotations_for_chat, name='annotations_for_chat'),

    path('', veutify_page, name='index'),
    path('cc/', veutify_page, name='vuetify_page'),
    path('docs', veutify_page, name='vuetify_page'),
    re_path(r'^cc/.*', veutify_page, name='vuetify_page'),
]
