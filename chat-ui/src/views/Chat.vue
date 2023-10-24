<template>
<v-app>
  <HeaderToolbar chat-noir-icon="@/assets/img/chanoir-icon.svg" @toggleDrawer="drawer = !drawer" />
  <NavigationDrawer v-model="drawer" />

  <loading :loading="loading"/>

  <v-container v-if="!loading" class="main-container mt-10 w-full">
    <v-row class="px-xl-16 d-block text-center">
      <div class="d-flex justify-space-between" v-if="messages.length > 0">
        <v-chip v-if="chatIsFinished" class="ma-2" color="success" variant="outlined" size="large">
          <v-icon start icon="mdi-text"></v-icon>
          Topic: {{ selectedTopic }}
        </v-chip>
        <v-btn
          v-if="!chatIsFinished"
          class="me-4"
          color=""
          icon="mdi-text-box-edit"
          @click="setChatisFinished"
        ></v-btn>
      </div>


      <v-select v-if="messages.length == 0 && chatIsFinished" label="Select your Topic"
                v-model="selectedTopic"
                :items="availableTopics"
                :v-if="chatIsFinished"
                item-title="title">
        <template v-slot:item="{ props}">
          <v-list-item v-bind="props">
          </v-list-item>
        </template>
      </v-select>


    </v-row>
    <v-row class="px-xl-16">
      <v-select v-if="!chatIsFinished" label="Select your Chatmodel" v-model="selectedChatModel"
                :items="chatModels" item-title="title" item-value="id">
        <template v-slot:item="{ props, item }">
          <v-list-item v-bind="props" :subtitle="item.raw.isRemovable">
            <template v-slot:append>
              <v-btn variant="text" v-if="item.raw.isRemovable" icon :onclick="() => removeChatModel(item.raw.id, item.raw.title)">
                <v-icon>mdi-trash-can-outline test</v-icon>
              </v-btn>
            </template>

          </v-list-item>
        </template>
        <template #append>
          <v-btn @click="addChatModelDialogueIsOpen = true">
            <v-icon>mdi-plus</v-icon>
          </v-btn>
        </template>
      </v-select>
    </v-row>

    <v-row class="px-xl-16" v-for="message in messages" :key="message.id">
      <ChatMessage :message="message" chat-noir-avatar="/assets/img/chatnoir-chat-avatar.svg"
                   :user-avatar="user.userAvatar"/>
    </v-row>
  </v-container>
  <AddChatmodelDialogue v-model="addChatModelDialogueIsOpen" :addNewChatModelFunction="addNewChatModel"/>

  <AssessmentArea v-if="chatIsFinished"
                  :conversationAnnotation="conversationAnnotation"
                  @update:conversationAnnotation="updateConversationAnnotation"
  />

  <FooterTextarea
    v-model="currentUserMessage"
    @send-message="sendMessage"
    @retry-message="retryMessage" v-if="(!loading && !chatIsFinished)"/>
</v-app>
</template>


<script lang="ts">
import { ref } from 'vue'
import Loading from "../components/Loading.vue"
import ChatMessage from "@/components/ChatMessage.vue";
import FooterTextarea from "@/components/FooterTextarea.vue";
import AddChatmodelDialogue from "@/components/AddChatmodelDialogue.vue";
import AssessmentArea from "@/components/AssessmentArea.vue";
import HeaderToolbar from "@/components/HeaderToolbar.vue";
import NavigationDrawer from "@/components/NavigationDrawer.vue";
import {get, post, avatar_src} from "@/utils";
import {ConversationAnnotation, Message} from '@/types';

function extractChatIdFromUrl() {
  let loc = ref(window.location).value.href.split('#')[0].split('?')[0]

  if (loc.includes('/cc/')) {
    return loc.split('/cc/')[1].split('/')[0]
  }

  return ''
}

export default {
  components: {HeaderToolbar, NavigationDrawer, AssessmentArea, AddChatmodelDialogue, ChatMessage, FooterTextarea, Loading},
  data: () => ({
    loading: true,
    selected_tags: [],
    addChatModelDialogueIsOpen: false,
    messages: [] as Message[],
    user: avatar_src(),
    drawer: false,
    selectedChatModel: "",
    chatModels: [{id: '0', title: 'loading....', isRemovable: true}],
    currentUserMessage: "",
    chatIsFinished: false,
    availableTopics: [' Web Track 2009', 'Obama family tree'],
    selectedTopic: "Obama family tree",
    conversationAnnotation: null as ConversationAnnotation | null,
    chat_id: extractChatIdFromUrl(),
    // utteranceAnnotations: null as UtteranceAnnotation[] | null,
  }),
  watch: {
    conversationAnnotation: {
      deep: true,
      handler() {
        console.log("conversationAnnotation changed: ", this.conversationAnnotation);
      }
    },
  },
  beforeMount() {
    if ('' + this.chat_id === 'undefined' || '' + this.chat_id === 'null' || '' + this.chat_id === '') {
      get('/load-chat-models', this)
      .then(() => {get('/load-chat/new-chat-id', this).then(this.updateUrl)});
    } else {
      get('/load-chat-models', this)
      .then(() => {get('/load-chat/' + this.chat_id, this).then(this.updateUrl)});
    }
  },
  methods: {
    setChatisFinished() {
      post('/finish-chat/' + this.chat_id, {}, this).then(() => {this.chatIsFinished = true});
    },
    updateUrl() {
			history.replaceState({'url': '/cc/' + this.chat_id}, 'ChatnoirChat', '/cc/' + this.chat_id);
      this.chat_id = extractChatIdFromUrl();
      
      if ('' + this.selectedChatModel === '' || '' + this.selectedChatModel === 'undefined' || '' + this.selectedChatModel === 'null') {
        this.selectedChatModel = this.chatModels[0]['id']
      }
    },

    sendMessage() {
      const message: Message = {id: this.messages.length, chat_id: this.chat_id,
                                text: this.currentUserMessage, type: "user", topic: this.selectedTopic,}

      post('/send-message/' + this.chat_id, {'message': this.currentUserMessage, 'endpoint': this.selectedChatModel}, this).then((m) => {
        this.messages.push(message);
        this.currentUserMessage = "";
        this.messages.push(m);
      });
    },
    addNewChatModel(title: string, description: string, backend_id: string) {
      console.log("add new chat model: ", title, description);

      post('/api/edit-custom-backend', {'title': title, 'description': description, 'backend_id': backend_id}, this)
      .then((newModel) => {
        this.chatModels.push(newModel);
        this.selectedChatModel = newModel.title;
      });
    },
    retryMessage() {
      //
    },
    removeChatModel(chatModelId: string, chatModelTitle: string) {
      this.chatModels = this.chatModels.filter((chatModel) => chatModel.title !== chatModelTitle)
      console.log("remove chat model: ", chatModelId);
      console.log("selectedChatModel: ", this.selectedChatModel);
      if (this.selectedChatModel === chatModelTitle) {
        this.selectedChatModel = "";
      }
      post('remove_chat_model', {'id': chatModelTitle}, this);
    },
    updateConversationAnnotation(updatedAnnotation: ConversationAnnotation) {
      this.conversationAnnotation = updatedAnnotation;
      console.log("Updated conversationAnnotation:", this.conversationAnnotation);
      post('/annotate-chat/' + this.chat_id, this.conversationAnnotation, this);
    }
  },
}
</script>


<style scoped>
.main-container {
  flex-grow: 1; /* take all available space */
  overflow-y: auto; /* scroll when content is too much */
  max-height: calc(100vh - 200px); /* Adjust based on the height of your textarea */
  max-width: 100% !important;
}

/* Mobile devices */
@media (max-width: 600px) {
  .main-container {
    width: 100%;
  }
}
</style>
