"""
Django test settings for chatnoir_chat project.
The test settings override original settings where required.
"""

from chatnoir_chat.settings import *

response_to_count = {}
def return_count(request):
    response_to_count[request] = response_to_count.get(request, 0) + 1
    return request + str(response_to_count[request])

STATIC_CHAT_ENDPOINTS['return_count'] = return_count