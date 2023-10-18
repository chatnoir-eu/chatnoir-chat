<template>
<div class="chat-index">
    <div class="chat-container">
        <div class="flex justify-between ml-3 mr-7 mt-2 items-center mb-2">
            <button class="flex justify-between items-center" @click="clearChat">
                <inline-svg :class="['h-full', 'mx-auto', 'align-middle', 'w-4',sendingIsDisabled ? 'disabled' : '']"
                            :src="require('@/assets/icons/reset.svg')">
                </inline-svg> &nbsp;Clear Session
            </button>
            <div>
                <div class="chatbot-backend-selector">
                    <select id="chatbot-backend" class="select" :value="selectedChatbotBackend" @change="onChatbotBackendChange($event)">
                        <option v-for="backend in chatbotBackends" :key="backend.display_name"
                                :value="backend.display_name">
                            {{ backend.display_name }}
                        </option>
                    </select>
                </div>
            </div>
        </div>
        <div ref="messages" class="chat-messages">
            <div v-for="(interaction, index) in interactions" :key="index"
                 :class="['chat-message', 'chat-message-' + interaction.type.toLowerCase()]">
                <div class="chat-message-avatar">
                    <template v-if="interaction.type !== 'user'">
                        <inline-svg :class="['h-full', 'mx-auto', 'w-10', 'align-middle']"
                                    :src="require('@/assets/img/chatnoir-chat-avatar.svg')">
                        </inline-svg>
                    </template>
                </div>
                <div class="chat-message-content">
                    <div class="chat-message-author flex items-center">
                        {{ interaction.type !== 'bot' ? '' : 'ChatNoir' }}
                        <button v-if="interaction.type === 'bot' && showExplanation !== index && index > 0" class="flex justify-between items-center ml-3" @click="showExplanation = index">
                            Explanation
                            <inline-svg :class="['h-full', 'mx-auto', 'w-4', 'align-middle', 'ml-2']"
                                        :src="require('@/assets/icons/arrow-down.svg')">
                            </inline-svg>
                        </button>
                        <button v-if="interaction.type === 'bot' && showExplanation === index" class="flex justify-between items-center ml-3" @click="showExplanation = false">
                            Explanation
                            <inline-svg :class="['h-full', 'mx-auto', 'w-4', 'align-middle', 'ml-2']"
                                        :src="require('@/assets/icons/arrow-up.svg')">
                            </inline-svg>
                        </button>
                    </div>
                    <div v-if="showExplanation === index">
                        <div class="modal-content">
                            <ul>
                                <li><b>Model:</b> {{ interaction.chatbot_backend }}</li>
                                <li><b>Description:</b> {{ interaction.description_of_generation }}</li>
                                <li><b>Rewritten Message:</b> {{ interaction.rewritten_message_text }}</li>
                            </ul>
                        </div>
                    </div>
                    <div class="chat-message-text">
                        {{ interaction.message }}
                        <div v-if="interaction.type === 'processing'" class="bubbles">
                            <span class="bubble"></span>
                            <span class="bubble"></span>
                            <span class="bubble"></span>
                        </div>
                    </div>
                </div>
            </div>
            <div v-if="searchResults.length > 0" id="search-results-mobile" class="text-lg">
                <div class="">
                    References:
                </div>
                <ol class="">
                    <li v-for="(result, searchRes) in searchResults" :key="searchRes" class="search-result-item">
                        <a :href="result.link">{{ result.headline }}</a>
                        <p>{{ result.description }}</p>
                    </li>
                </ol>
            </div>
        </div>
        <div class="disclaimer">
            Disclaimer: This is a research prototype and for demonstration purposes only.
        </div>
        <div class="chat-input">
            <textarea id="message-input" ref="textarea" v-model="messageInput" type="text" placeholder="Type a message..."
                      @keydown.enter="handleSubmitMessageOnEnter"
            />
            <button :disabled="sendingIsDisabled" @click="sendMessage">
                <inline-svg
                    :class="['h-full', 'mx-auto', 'align-middle', 'w-6',sendingIsDisabled ? 'disabled' : '']"
                    :src="require('@/assets/icons/send-fill.svg')"
                    alt="Search" />
            </button>
        </div>
    </div>
    <div class="references-container">
        <div class="mt-5">
            <div v-if="searchResults.length > 0" id="search-results-desktop" class="text-lg">
                <div class="">
                    The last response of ChatNoir was based on these references:
                </div>
                <ol class="mt-5">
                    <li v-for="(result, searchRes) in searchResults" :key="searchRes" class="search-result-item">
                        <a :href="result.link">{{ result.headline }}</a>
                        <p>{{ result.description }}</p>
                    </li>
                </ol>
            </div>
        </div>
    </div>
</div>

<confirm-modal
    :is-open="showConfirmModal"
    message="Changing the model will clear the current chat session. Are you sure?"
    @confirmed="onModalConfirmed"
    @canceled="onModalCanceled"
></confirm-modal>
</template>

<script>
import axios from "axios";
import Vue from "@/main";
import {nextTick} from "vue";
import {v4 as uuidv4} from 'uuid';
import ConfirmModal from "@/components/ConfirmModal.vue";

axios.defaults.headers.post['Content-Type'] = 'application/json';

export default {
    components: {ConfirmModal},

    data() {
        return {
            interactions: [],
            searchResults: [
                {link: "http://google.de", headline: "Google", description: "Search engine"},
                {link: "http://google.de", headline: "Google", description: "Search engine"},
            ],
            // searchResults: [],
            messageInput: '',
            showExplanation: false,
            chatbotBackends: [{display_name: 'Alpaca (7B)'}, {display_name: "GPT-2 (117M)"}, {display_name: "dummycode, remove this"}],
            selectedChatbotBackend: null,
            lastPollTime: null,
            sendingIsDisabled: false,
            showConfirmModal: false,
            selectedValueBackends: null,
        };
    },
    created() {
        this.fetchChatbotBackends();
    },

    methods: {
        onModalConfirmed() {
            this.changeBackend(this.selectedValueBackends);
            this.showConfirmModal = false;
        },

        onModalCanceled() {
            this.showConfirmModal = false;
        },

        onChatbotBackendChange(event) {
            this.selectedValueBackends = event.target.value;
            if (this.interactions.length > 1) {
                this.showConfirmModal = true;
            } else {
                this.changeBackend(this.selectedValueBackends);
            }
        },
        changeBackend(selectedBackend) {
            // // console.log("change backend. backend: " + selectedBackend);
            this.selectedChatbotBackend = selectedBackend;
            this.clearChat();
        },
        handleSubmitMessageOnEnter(event) {
            if (!event.shiftKey) {
                event.preventDefault();
                this.sendMessage();
            }
        },
        clearChat() {
            // console.log("clear chat. backend: " + this.selectedChatbotBackend);
            const formData = new FormData();
            formData.append('chatbot_backend', this.selectedChatbotBackend);

            // Send a POST request to the Django server to store the new message and get the bot response
            axios
                .post('/chat/clear-chat', formData, {
                    headers: {
                        'X-CSRFToken': window.DATA.csrfToken,
                        'Content-Type': 'multipart/form-data',
                    },
                })
                .then((response) => {
                    if (response.data.status === 'success') {
                        // Clear the chat history in the frontend
                        window.DATA.csrfToken = response.data.new_csrf_token;
                        this.lastPollTime = null;
                        this.searchResults = [];
                        this.fetchInteractions();
                    }
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        fetchInteractions() {
            axios
                .get('/chat/interactions', {headers: {'Accept': 'application/json', 'X-CSRFToken': window.DATA.csrfToken}})
                .then((response) => {
                    if (this.selectedChatbotBackend === null) {
                        if (response.data.selected_chatbot_backend === null) {
                            this.selectedChatbotBackend = this.chatbotBackends[0].display_name;
                        } else {
                            this.selectedChatbotBackend = response.data.selected_chatbot_backend;
                        }
                    }

                    // Add the actual bot response(s) to the interactions array
                    this.interactions = [{type: 'bot', message: 'Bonjour! I\'m ChatNoir, your friendly cat assistant. How can I help you today?'}];
                    this.interactions.push(...response.data.interactions);

                    if (response.data.interactions.length > 0) {
                        this.lastPollTime =
                            response.data.interactions[response.data.interactions.length - 1]
                                .timestamp;
                    }
                    
                    if (this.interactions.length > 1) {
                        let last_interaction = this.interactions[this.interactions.length - 1]
                        this.searchResults = JSON.parse(last_interaction.search_results)
                    }
                })
                .catch((error) => {
                    console.error(error);
                }).finally(() => {
                    this.sendingIsDisabled = false;
                });
            nextTick(() => {
                this.scrollToBottom();
            });
        },
        sendMessage() {
            if (this.messageInput.trim().length > 0 && !this.sendingIsDisabled) {
                // // // console.log("send message. backend: " + this.selectedChatbotBackend);
                this.sendingIsDisabled = true;
                // Add user's message to the interactions array
                this.interactions.push({type: 'user', message: this.messageInput.trim()});

                // Add a loading message bubble to the interactions array
                this.interactions.push({
                    type: 'processing',
                    message: 'Preparing response...',
                });

                // Create a FormData object
                const formData = new FormData();
                formData.append('message', this.messageInput);
                formData.append('chatbot_backend', this.selectedChatbotBackend);

                // Send a POST request to the Django server to store the new message and get the bot response
                axios
                    .post('/chat/interactions', formData, {
                        headers: {
                            'X-CSRFToken': window.DATA.csrfToken,
                            'Content-Type': 'multipart/form-data',
                        },
                    })
                    .then(() => {
                        this.fetchInteractions();
                    })
                    .catch((error) => {
                        console.error(error);
                    });

                this.messageInput = '';
                // this.resetTextArea();

                nextTick(() => {
                    this.scrollToBottom();
                });
            }
        },
        scrollToBottom() {
            const messagesContainer = this.$refs.messages;
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        },
        resizeTextArea() {
            const textarea = this.$refs.textarea;
            textarea.style.height = 'auto';
            textarea.style.height = Math.min(textarea.scrollHeight, 100) + 'px'; // Set a max height of 100px
        },
        resetTextArea() {
            const textarea = this.$refs.textarea;
            textarea.style.height = 'auto';
            textarea.style.height = '30px'; // Set a minimum height of 30px
        },
        fetchChatbotBackends() {
            axios.get('/chat/chatbot-backends', {headers: {'Accept': 'application/json'}})
                .then((response) => {
                    this.chatbotBackends = response.data.backends;
                    this.fetchInteractions();
                })
                .catch((error) => {
                    console.error(error);
                });
        },
    }
}
    
</script>

<style scoped>

body {
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
}



.message-input {
    height: 60px;
}

/*desktop version*/
@media only screen and (min-width: 768px) {
    .chat-index {
        /*  translate this: "flex flex-row space-x-10" into css*/
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        /*margin: 0 auto;*/
    }
    #search-results-desktop {
        display: block;
    }

    #search-results-mobile {
        display: None;
    }

    .chat-container {
        display: flex;
        flex-direction: column;
        height: 100%;
        margin: 0 5rem 0 auto;
        max-width: 55vw; /* or any other value you prefer */
        max-height: 85vh; /* Subtract chat window height */
    }

    .references-container {
        display: flex;
        flex-direction: column;
        height: 100%;
        margin: 0 auto;
        max-height: 85vh; /* Subtract chat window height */
    }
}

/*mobile version*/
@media only screen and (max-width: 767px) {
#search-results-desktop {
    display: None;
}

#search-results-mobile {
    display: block;
    }

.chat-index {
    /*  in this case we are on a mobile screen therefore the child elements are to be rendered below each other*/
    flex-direction: column;
}


.chat-container {
    margin-left: 20px;
    margin-right: 20px;
}

.references-container {
    margin-left: 20px;
    margin-right: 20px;
}

}

.disabled {
    opacity: 0.5;
    pointer-events: none;
}

.search-result-item {
    margin-bottom: 20px;
}

.chat-messages {
    flex: 1;
    height: 100%;
    overflow-y: auto;
    padding: 10px;
}

.chat-message {
    display: flex;
    align-items: flex-start;
    /*align-items: center;*/
    margin-bottom: 10px;
    padding: 10px;
    border-radius: 10px;
    border: 1px solid #f1f0f0;
    font-size: 1.1em;

}

.chat-message-bot, .chat-message-processing {
    background-color: #f1f0f0;
    margin-right: 20px;
        min-width: 40vw;
}


.chat-message-user {
    background-color: #f1f0f0;
    align-self: flex-end;
    text-align: right;
    margin-left: 20px;
}


.chat-message-bot .chat-message-avatar {
    margin-right: 10px;
}

.chat-message-user .chat-message-avatar {
    margin-left: 10px;
}

.chat-message-bot .chat-message-content {
    flex: 1;
}

.chat-message-user .chat-message-content {
    flex: 1;
    text-align: right;
}

.chat-message-bot .chat-message-text {
    color: #d2725b;
}

.disclaimer {
    padding-top: 0.5em;
    paddin-left:0.2em;
    font-size: 0.8em;
    color: #d2725b;
}

.chat-message-user .chat-message-text {

}

.chat-message-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    overflow: hidden;
}

.chat-message-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.chat-message-avatar .inline-svg {
    width: 100%;
    height: 100%;
}

.chat-message-content {
    flex: 1;
}

.chat-message-author {
    font-weight: bold;
}

.chat-input {
    border: 1px solid #f1f0f0;
    border-radius: 10px;
    display: flex;
    padding: 10px;
    /*overflow-y: auto;*/
    height: auto;
    min-height: 34px;
    max-height: 130px;
}

.chat-input textarea {
    flex: 1;
    margin-right: 10px;
    overflow-y: scroll;
    height: auto;
    min-height: 34px;
    max-height: 102px;
    resize: none;
}


.chat-input textarea:focus {
    outline: none;
}


.chat-input button {
    width: 50px;
}

@keyframes moving-bubbles {
    0% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-10px);
    }
    100% {
        transform: translateY(0);
    }
}

.bubble {
    display: inline-block;
    width: 6px;
    height: 6px;
    background-color: #333;
    border-radius: 50%;
    margin: 0 2px;
    animation: moving-bubbles 1s ease-in-out infinite;
}

.bubble:nth-child(2) {
    animation-delay: 0.2s;
}

.bubble:nth-child(3) {
    animation-delay: 0.4s;
}


footer {
    height: 80px;
    background-color: #f1f0f0;
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>

