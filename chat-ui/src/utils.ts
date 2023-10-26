// types

import {ConversationAnnotation, UtteranceAnnotation} from "@/types";

type ChatHistory = {
	chatHistory: { link: string; title: string }[];
};

type ChatModels = {
	chatModels: { id: string; title: string; isRemovable: boolean }[];
	selectedChatModel: string;
};

type EndpointPythonCode = {
	endpointPythonCode: string;
};

type ChatMessage = {
	id: number;
	text: string;
	type: 'bot' | 'user';
	topic: string;
	chat_id: string;
};

type Chat = {
	messages: ChatMessage[];
	userAvatar: string;
	loading: boolean;
	selectedChatModel: string;
	availableTopics: string[];
	selectedTopic: string;
	chatIsFinished: boolean;
	chatModels: { id: string; title: string; isRemovable: boolean }[];
	conversationAnnotation: ConversationAnnotation;
	utteranceAnnotations: UtteranceAnnotation[];
};


type ApiValue =
	| ChatHistory
	| ChatModels
	| Chat
	| EndpointPythonCode
	| ConversationAnnotation
	| UtteranceAnnotation[]
	| ((data: any) => Promise<any>);


// Mock data
const MOCK_CHAT_HISTORY = {'chatHistory': [{link: '/cc/1', title: 'Chat 1'}, {link: '/cc/2', title: 'Chat 2'}]};

const MOCK_CHAT_MODELS = {
	'chatModels': [{id: '0', title: 'Alpaca-7B', isRemovable: true}, {id: '1', title: 'GPT-2', isRemovable: true}],
	'selectedChatModel': '0'
}

const MOCK_CONVERSATION_ANNOTATION: ConversationAnnotation = [
	{
		question_id: '0',
		question_text: 'Did the model answer your question based on facts?',
		response_type: 'Yes/No',
		answer: null
	},
	{
		question_id: '1',
		question_text: 'Does the model remember the context of the conversation?',
		response_type: 'Yes/No',
		answer: null
	},
];

const MOCK_UTTERANCE_ANNOTATIONS: UtteranceAnnotation[] = [
	{
		"utterance_id": 0,
		"questions": [
			{
				"question_id": "0",
				"question_text": "Was the answer helpful?",
				"response_type": "Yes/No",
				"answer": null
			},
			{
				"question_id": "1",
				"question_text": "Was this response based on facts?",
				"response_type": "Yes/No",
				"answer": null
			},
		]
	},
	{
		"utterance_id": 1,
		"questions": [
			{
				"question_id": "0",
				"question_text": "Was the answer helpful?",
				"response_type": "Yes/No",
				"answer": null
			},
			{
				"question_id": "1",
				"question_text": "Was this response based on facts?",
				"response_type": "Yes/No",
				"answer": null
			}
		]
	},
]


const MOCK_ENDPOINT_PYTHON_CODE = {
	'endpointPythonCode':
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
	{
		id: 2,
		text: "Barack Obama`s wife is Michelle Obama and his daughters are Sasha and Malia.",
		type: 'bot',
		topic: '',
		chat_id: ''
	},
	{id: 3, text: "How old are they?", type: 'user', topic: '', chat_id: ''}
];

const MOCK_CHAT = {
	messages: MOCK_CHAT_MESSAGES,
	userAvatar: "https://randomuser.me/api/portraits/men/78.jpg",
	loading: false,
	selectedChatModel: '0',
	availableTopics: [' Web Track 2009', 'Obama family tree'],
	selectedTopic: "Obama family tree",
	chatIsFinished: false,
	chatModels: MOCK_CHAT_MODELS.chatModels,
	conversationAnnotation: MOCK_CONVERSATION_ANNOTATION,
	utteranceAnnotations: MOCK_UTTERANCE_ANNOTATIONS,
	chatId: 'adfejkalej324'
}


const API_CALLS: Record<string, ApiValue> = {
	'/load-chat-history': MOCK_CHAT_HISTORY,
	'/load-chat-models': MOCK_CHAT_MODELS,
	'/load-chat/': MOCK_CHAT,
	'/load-chat/new-chat-id': MOCK_CHAT, // this is the enpoint to create a new chat
	'/load-add-endpoint-code': MOCK_ENDPOINT_PYTHON_CODE,
	'/load-conversation-annotation': MOCK_CONVERSATION_ANNOTATION,
	'/load_utterance-annotations': MOCK_UTTERANCE_ANNOTATIONS,
	'/send-message': async (data: any) => {
		return {
			'id': Math.random(),
			'chat_id': data['chat_id'],
			'text': "You said: " + data['text'],
			'type': 'bot',
			'topic': ''
		}
	},
	'/new-chat-model': async (data: any) => {
		return {'id': Math.random().toString(), title: data['title'], 'isRemovable': true}
	},
	'/remove-chat-model': async (data: any) => {
		return {'id': data['id']}
	}
}


async function mockApiCall(url: string, obj: any = null, delay: number = 1000): Promise<any> {
	let ret: any = null;

	for (const endpoint of Object.keys(API_CALLS)) {
		if (url.includes(endpoint)) {
			const apiFunction = API_CALLS[endpoint];
			if (obj === null) {
				ret = apiFunction;
			} else {
				if (apiFunction instanceof Function) {
					ret = apiFunction(obj);

				} else {
					ret = apiFunction;
				}

			}

			break
		}
	}

	await new Promise(resolve => setTimeout(resolve, delay));
	return ret;
}

export function avatar_src(): { userAvatar: string; userName: string } {
	try {
		const elem = document.querySelector('img.avatar');
		// @ts-ignore
		return {'userAvatar': elem.src, 'userName': elem.title}
	} catch (exception) {
		return {'userAvatar': 'https://webis.de/weimar/people/img/silhouette-female.jpg', 'userName': 'Unregistered User'}
	}
}

// @ts-ignore
window.avatar_src = avatar_src

function default_values(): { userAvatar: string; userName: string; loading: boolean } {
	const ret = avatar_src();
	// @ts-ignore
	ret['loading'] = false;
	// @ts-ignore
	return ret;
}

function inject_response(response: any, obj: any): void {
	const defaults = default_values();

	if (response != null) {
		console.log('response: ' + response)
		for (const k of Object.keys(response)) {
			// @ts-ignore
			// eslint-disable-next-line no-prototype-builtins
			if (response.hasOwnProperty(k) && obj.$data.hasOwnProperty(k)) {
				console.log('copy property ' + k)
				obj.$data[k] = response[k]
			}
		}

		for (const k of Object.keys(defaults)) {
			// eslint-disable-next-line no-prototype-builtins
			if (obj.$data.hasOwnProperty(k)) {
				// @ts-ignore
				obj.$data[k] = defaults[k]
			}
		}
	}
}

export function extractCsrf(doc: Document = document): string {
	try {
		const ret = doc.querySelector('input[type="hidden"][name="csrfmiddlewaretoken"][value]')
		if (ret && 'value' in ret) {
			return "" + ret['value']
		}
	} catch {
		console.error('Could not extract csrf token.')
	}

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
	return await response.json()

}

async function execute_post(url: string, obj: any): Promise<any> {
	const headers = new Headers({
		'Accept': 'application/json',
		'Content-Type': 'application/json',
		'X-CSRFToken': extractCsrf(),
		'X-Disraptor-Groups': 'chatnoir_chat___echo,',
		'X-Disraptor-App-Secret-Key': 'no-secret-key'
	})
	const response = await fetch(url, {method: 'POST', headers: headers, body: JSON.stringify(obj)})

	if (!response.ok) {
		throw new Error(`Error fetching endpoint: ${url} with ${response.status}`);
	}
	return await response.json()

}

const get_method = import.meta.env.DEV ? mockApiCall : execute_get;
const post_method = import.meta.env.DEV ? mockApiCall : execute_post;

export async function get(url: string, obj: any): Promise<any> {
	const response = await get_method(url);

	if (response == null) {
		console.error(`Unknown endpoint: ${url}`);
	}

	inject_response(response, obj);
	return response;
}

export async function post(url: string, data: any, obj: any): Promise<any> {
	const response = await post_method(url, data);
	console.log("post, url: " + url + ", data: " + data + ", response: " + response);
	inject_response(response, obj);
	return response
}
