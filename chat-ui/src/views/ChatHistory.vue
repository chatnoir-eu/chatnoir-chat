<template>
<div class="chat-index">
    <div class="chat-container">
        <div v-if="!is_authenticated">
            <h1>Welcome to the Chat Integration of ChatNoir</h1>
            
            You can start to chat <a href="/chat-ui">here</a>. If you <a href="/login">sign in</a>, you get a history of all your chats and you can give feedback to chats and responses that you can extract via an API.
        </div>
        <div v-else>
            <h1>Welcome {{ user_name }}!</h1>
        </div>
    </div>
</div>
</template>

<script>
import axios from "axios";
import Vue from "@/main";
import {nextTick} from "vue";
import {v4 as uuidv4} from 'uuid';

axios.defaults.headers.post['Content-Type'] = 'application/json';

export default {

    data() {
        return {
            is_authenticated: false,
            user_name: '',
            chat_history: [],
        };
    },
    created() {
        //this.fetchChatbotBackends();
    },

    methods: {
    }
}
    
</script>

<style scoped>
html, body {
    height: 100%;
}

body {
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    min-height: calc(100vh - 80px); /* Subtract chat window height */
}

.chat-index {
    /*  in this case we are on a mobile screen therefore the child elements are to be rendered below each other*/
    flex-direction: column;
}


.chat-container {
    margin-left: 20px;
    margin-right: 20px;
}

@media only screen and (min-width: 768px) {
    .chat-index {
        /*  translate this: "flex flex-row space-x-10" into css*/
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        /*margin: 0 auto;*/
        height: 100%
    }

    .chat-container {
        display: flex;
        flex-direction: column;
        height: 100%;
        margin: 0 5rem 0 auto;
        max-width: 48vw; /* or any other value you prefer */
        max-height: calc(100vh - 80px); /* Subtract chat window height */
    }

    .references-container {
        display: flex;
        flex-direction: column;
        height: 100%;
        margin: 0 auto;
        max-height: calc(100vh - 80px); /* Subtract chat window height */
    }
}

.disabled {
    opacity: 0.5;
    pointer-events: none;
}

footer {
    height: 80px;
    background-color: #f1f0f0;
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>

