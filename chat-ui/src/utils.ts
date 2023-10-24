// Mock data
const MOCK_CHAT_HISTORY = {'chatHistory': [{link: '/cc/1', title: 'Chat 1'}, {link: '/cc/2', title: 'Chat 2'}]};

const MOCK_CHAT_MODELS = {
	'chatModels': [{id: '0', title: 'Alpaca-7B', isRemovable: true}, {id: '1', title: 'GPT-2', isRemovable: true}],
	'selectedChatModel': 'Alpaca-7B'
}

const MOCK_CONVERSATION_ANNOTATION = {'conversationAnnotation': [
	{question_id: '0', question_text: 'Did the model answer your question based on facts?', response_type: 'Yes/No', answer: null},
	{question_id: '1', question_text: 'Does the model remember the context of the conversation?', response_type: 'Yes/No', answer: null},
]};

const MOCK_ENDPOINT_PYTHON_CODE = {'endpointPythonCode': 
	`class BasicUIMeta(metaclass=abc.ABCMeta):
          @abc.abstractmethod
          def click(self, x: int, y: int):
              pass

          @abc.abstractmethod
          def swipe(self, fx: int, fy: int, tx: int, ty: int, duration: float):
              """ duration is float type, indicate seconds """

          @abc.abstractmethod
          def window_size(self) -> tuple:
              """ return (width, height) """
              `
}

const MOCK_CHAT_MESSAGES = [
	{id: 0, text: "Hi, I am ChatCat your friendly Cat assistant.", type: 'bot', topic: '', chat_id: ''},
	{id: 1, text: "Hello, can you tell me who the wife of barack obama is?", type: 'user', topic: '', chat_id: ''},
	{id: 2, text: "Barack Obama`s wife is Michelle Obama and his daughters are Sasha and Malia.", type: 'bot', topic: '', chat_id: ''},
	{id: 3, text: "How old are they?", type: 'user', topic: '', chat_id: ''}
];

const MOCK_CHAT = {
	messages: MOCK_CHAT_MESSAGES,
	userAvatar: "https://randomuser.me/api/portraits/men/78.jpg",
	loading: false,
	selectedChatModel: 'Alpaca-7B',
	availableTopics: [' Web Track 2009', 'Obama family tree'],
	selectedTopic: "Obama family tree",
	chatIsFinished: false,
	chatModels: MOCK_CHAT_MODELS.chatModels,
	conversationAnnotation: MOCK_CONVERSATION_ANNOTATION.conversationAnnotation,
}

const API_CALLS = {
	'/load-chat-history': MOCK_CHAT_HISTORY, '/load-chat-models': MOCK_CHAT_MODELS, '/load-chat/': MOCK_CHAT,
	'/load-add-endpoint-code': MOCK_ENDPOINT_PYTHON_CODE, '/load-conversation-annotation': MOCK_CONVERSATION_ANNOTATION,
	'/send-message': async (data: any) => {return {'id': Math.random(), 'chat_id': data['chat_id'], 'text': "You said: " + data['text'], 'type': 'bot', 'topic': ''}},
	'/new-chat-model': async (data: any) => {return {'chatModel': {'id': Math.random(), title: data['title'], 'isRemovable': true}}},
}

async function mockApiCall(url: string, obj: any=null, delay=1000) {
	let ret: any = null;

	for (const endpoint of Object.keys(API_CALLS)) {
		if (url.includes(endpoint)) {
			ret = (obj === null) ? API_CALLS[endpoint] : API_CALLS[endpoint](obj);
			break
		}
	}

	await new Promise(resolve => setTimeout(resolve, delay));
	return ret;
}

export function avatar_src(): { [key: string]: any } {
	try {
		const elem = document.querySelector('img.avatar');
		return {'userAvatar': elem.src, 'userName': elem.title}
	} catch (exception) {
		return {'userAvatar': 'https://webis.de/weimar/people/img/silhouette-female.jpg', 'userName': 'Unregistered User'}
	}
}

window.avatar_src = avatar_src

function default_values(): { [key: string]: any } {
	const ret = avatar_src();
	ret['loading'] = false;
	return ret;
}

function inject_response(response:any, obj:any) {
	const defaults = default_values();

	if (response != null) {
		console.log('response: ' + response)
		for (const k of Object.keys(response)) {
			if(response.hasOwnProperty(k) && obj.$data.hasOwnProperty(k)) {
				console.log('copy property ' + k)
				obj.$data[k] = response[k]
			}
		}

		for (const k of Object.keys(defaults)) {
			if(obj.$data.hasOwnProperty(k)) {
				obj.$data[k] = defaults[k]
			}
		}
	}
}

export function extractCsrf(doc: Document=document) : string {
    try  {
        var ret = doc.querySelector('input[type="hidden"][name="csrfmiddlewaretoken"][value]')
        if (ret && 'value' in ret) {
            return "" + ret['value']
        }
    } catch { }

    return ''
}

async function execute_get(url: string) {
    const response = await fetch(url, {
		method: 'GET',
		headers: {'X-Disraptor-Groups': 'chatnoir_chat___echo,', 'X-Disraptor-App-Secret-Key': 'no-secret-key'},
	  })

    if (!response.ok) {
      throw new Error(`Error fetching endpoint: ${url} with ${response.status}`);
    }
    let results = await response.json()

    return results
}

async function execute_post(url: string, obj: any) {
    const headers = new Headers({'Accept': 'application/json', 'Content-Type': 'application/json', 'X-CSRFToken': extractCsrf(), 'X-Disraptor-Groups': 'chatnoir_chat___echo,', 'X-Disraptor-App-Secret-Key': 'no-secret-key'})
    const response = await fetch(url, {method: 'POST', headers: headers, body: JSON.stringify(obj)})

    if (!response.ok) {
      throw new Error(`Error fetching endpoint: ${url} with ${response.status}`);
    }
    let results = await response.json()

    return results
}

const get_method = import.meta.env.DEV ? mockApiCall : execute_get;
const post_method = import.meta.env.DEV ? mockApiCall : execute_post;

export async function get(url: string, obj: any) {
	let response = await get_method(url);

	if (response == null) {
		console.error(`Unknown endpoint: ${url}`);
	}

	inject_response(response, obj);
	return response;
}

export async function post(url: string, data: any, obj: any) {
	let response = await post_method(url, data);
	inject_response(response, obj);
	return response
}
