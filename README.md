# ChatCat: Your Friendly Cat Assistant

ChatCat (currently under review) is a software suite consisting of a library server, API, and web frontend for conducting laboratory experiments and user studies with generative retrieval systems. You can try it [online](https://chat.web.webis.de/) or watch a short [screencast](https://chat.web.webis.de/t/screencast-of-chatcat).

Components:
- [chat-backend](chat-backend) contains the server backend
- [chat-ui](chat-ui) contains the user interface
- [custom-backends](custom-backends) dynamically add new chat backends via websockets
- [chatnoir-api](api-support) provides an API client to chat with the cat
- [llms](llms) the supported llms that are available (you can dynamically add more via [custom-backends](custom-backends))

### Custom Backends

ChatCat has a focus on research-oriented laboratory experiments, so you can dynamically connect custom backends and/or pipelines for generative retrieval systems. Please see the [tutorial on how to add a custom backend](custom-backends). We also provide a set of [recipies/example backends](custom-backends/recipies) that are always available online.


### API Support

You can access the LLMs in ChatCat via an [API](https://github.com/chatnoir-eu/chatnoir-api).
The models `alpaca-en-7b` and `gpt2-xl` are public and do not require an API-Key, for other models (including [custom backends](custom-backends)), you need an API key for authentication (please request one from the [admins](mailto:maik.froebe@uni-jena.de)).

For python, we provide a client library so that you can chat with the cat:
```
from chatnoir_api.chat import ChatNoirChatClient

chat_client = ChatNoirChatClient()
response = chat_client.chat("how are you?")
```

