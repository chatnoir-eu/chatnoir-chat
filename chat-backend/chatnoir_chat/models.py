from django.db import models
import django.utils.timezone as timezone

class RequestAndResponseCache(models.Model):
    user_id = models.CharField(max_length=100, db_index=True)
    md5_hash_of_request = models.CharField(max_length=280, db_index=True)
    endpoint = models.CharField(max_length=150)
    date = models.DateTimeField(default=timezone.now)
    seed = models.CharField(max_length=50, db_index=True)
    request_text = models.TextField(default="", max_length=None)
    response_text = models.TextField(default="", max_length=None)

class Chat(models.Model):
    chat_id = models.CharField(max_length=150, primary_key=True)
    display_name = models.CharField(max_length=50, default='Unnamed Chat')
    description = models.TextField(default='No description available')
    deleted = models.BooleanField(default=False)   
    user_id = models.CharField(max_length=100, db_index=True)
    is_finished = models.BooleanField(default=False)

class ChatMessage(models.Model):
    message_id = models.AutoField(primary_key=True)
    chat = models.ForeignKey(Chat, on_delete=models.RESTRICT, null=False, db_index=True)
    text = models.TextField(max_length=None)
    type = models.CharField(max_length=10)
    endpoint = models.CharField(max_length=150)

class CustomBackends(models.Model):
    backend_id = models.CharField(max_length=150, primary_key=True)
    display_name = models.CharField(max_length=50, default='Unnamed Backend')
    description = models.CharField(max_length=50, default='Please add a description.')
    deleted = models.BooleanField(default=False)
    user_id = models.CharField(max_length=100, db_index=True)
