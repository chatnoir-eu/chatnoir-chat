<template>
  <v-app class="d-flex flex-column app-container">
    <NavigationDrawer v-model="drawerIsOpen"/>
    <loading :loading="loading"/>
    <v-container v-if="!loading" class="main-container w-full pt-0">
      <v-row class="pt-2">
        <topic-overview :ir_dataset="annotation_dataset" :topic_num="annotation_topic"/>
      </v-row>

      <v-row class="px-xl-16" v-for="message in messages" :key="message.id">
        <ChatMessage
          chat-noir-avatar="../assets/img/chatnoir-chat-avatar.svg"
          :isSelectable="annotationView === 'utterance'"
          :selectedMessageId="currentAnnotationMessageId"
          :message="message"
          :user-avatar="user.userAvatar"
          @update:currentAnnotationMessageId="updateCurrentAnnotationMessageId"
        />
      </v-row>
      <v-row class="px-xl-16" v-if="messageIsLoading">
        <v-col class="d-flex">
          <v-card class="me-2 rounded-b-shaped w-100">
            <v-toolbar
              density="compact"
              color="white"
            >

              <template #prepend>
                <template>
                  <v-avatar
                    class="mr-2"
                    color="white"
                    image="../assets/img/chatnoir-chat-avatar.svg"></v-avatar>
                  ChatCat
                </template>
              </template>

            </v-toolbar>
            <v-list-item>
              <v-card-text>
                <loading :loading="messageIsLoading"/>
                Retrieving message...
              </v-card-text>
            </v-list-item>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <AddChatmodelDialogue v-model="addChatModelModalIsOpen" :addNewChatModelFunction="addNewChatModel"/>
    <ChatSettings
      v-if="chatSettingsModalIsOpen"
      v-model="chatSettingsModalIsOpen"
      :chatModels="chatModels"
      :chatIsFinished="chat_is_finished"
      :chatId="chat_id"
      @updateChatTitle="chat_title = $event"
      @updateChatDescription="chat_description = $event"
      @updateSelectedChatModel="selectedChatModel = $event"
      @removeChatModel="removeChatModel"
      @openAddChatModelDialogue="addChatModelModalIsOpen = true"
    />

    <AssessmentArea v-if="chat_is_finished" :selectedMessageId="currentAnnotationMessageId"
                    :annotationView="annotationView" :chatId="chat_id"
                    @update:annotationView="annotationView = $event" @toggle-drawer="drawerIsOpen = !drawerIsOpen"
    />

    <FooterTextarea
      v-model="currentUserMessage"
      v-if="(!loading && !chat_is_finished)"
      :selectedChatModel="selectedChatModelTitle"
      @send-message="sendMessage"
      @retry-message="retryMessage"
      @set-chat-is-finished="setChatisFinished"
      @open-settings-modal="openSettingsModal"
      @toggle-drawer="drawerIsOpen = !drawerIsOpen"
    />
  </v-app>
</template>


<script lang="ts">
import {ref} from 'vue'
import Loading from "../components/Loading.vue"
import ChatMessage from "@/components/ChatMessage.vue";
import FooterTextarea from "@/components/FooterTextarea.vue";
import AddChatmodelDialogue from "@/components/AddChatmodelDialogue.vue";
import AssessmentArea from "@/components/AssessmentArea.vue";
import NavigationDrawer from "@/components/NavigationDrawer.vue";
import {get, post, avatar_src} from "@/utils";
import {ConversationAnnotation, Message, UtteranceAnnotation} from '@/types';
import ChatSettings from "@/components/ChatSettings.vue";
import TopicOverview from "@/components/TopicOverview.vue";


function extractChatIdFromUrl() {
  let loc = ref(window.location).value.href.split('#')[0].split('?')[0]

  if (loc.includes('/cc/')) {
    return loc.split('/cc/')[1].split('/')[0]
  }

  return ''
}

export default {
  components: {ChatSettings, NavigationDrawer, AssessmentArea, AddChatmodelDialogue,
               ChatMessage, FooterTextarea, Loading, TopicOverview
  },
  computed: {
    selectedChatModelTitle() {
      // Check if chatModels has data and selectedChatModel is set
      if (this.chatModels.length && this.selectedChatModel) {
        const filteredModels = this.chatModels.filter((chatModel) => chatModel.id === this.selectedChatModel);
        return filteredModels.length > 0 ? filteredModels[0].title : "Not selected yet";
      }
      return "Loading..."; // or any placeholder text you prefer
    }
  },

  data: () => ({
    loading: true,
    addChatModelModalIsOpen: false,
    chatSettingsModalIsOpen: false,
    messages: [] as Message[],
    user: avatar_src(),
    drawerIsOpen: false,
    selectedChatModel: "",
    chatModels: [{id: '0', title: 'loading....', isRemovable: true}],
    currentUserMessage: "",
    chat_is_finished: false,
    chat_id: extractChatIdFromUrl(),
    chat_title: "",
    chat_description: "",
    annotationView: "conversation",
    annotation_dataset: null,
    annotation_topic: null,
    currentAnnotationMessageId: -1,
    messageIsLoading: false,
  }),
  beforeMount() {
    if ('' + this.chat_id === 'undefined' || '' + this.chat_id === 'null' || '' + this.chat_id === '') {
      get('/load-chat-models', this)
        .then(() => {
          get('/load-chat/new-chat-id', this).then(this.updateUrl)
        });
    } else {
      get('/load-chat-models', this)
        .then(() => {
          get('/load-chat/' + this.chat_id, this).then(this.updateUrl)
        });
    }
  },
  methods: {
    setChatisFinished() {
      post('/configure-chat/' + this.chat_id, {'is_finished': true}, this).then(() => {
        this.chat_is_finished = true
      });
    },
    updateUrl() {
      history.replaceState({'url': '/cc/' + this.chat_id}, 'ChatnoirChat', '/cc/' + this.chat_id);
      this.chat_id = extractChatIdFromUrl();

      if ('' + this.selectedChatModel === '' || '' + this.selectedChatModel === 'undefined' || '' + this.selectedChatModel === 'null') {
        this.selectedChatModel = this.chatModels[0]['id']
      }
    },

    sendMessage() {
      const message: Message = {
        id: this.messages.length, chat_id: this.chat_id,
        text: this.currentUserMessage, type: "user",
      }
      this.messages.push(message);
      this.messageIsLoading = true;

      post('/send-message/' + this.chat_id, {
        'message': this.currentUserMessage,
        'endpoint': this.selectedChatModel
      }, this).then((m) => {

        this.currentUserMessage = "";
        this.messages.push(m);
        this.messageIsLoading = false;
      });
    },
    addNewChatModel(title: string, description: string, backend_id: string) {
      post('/new-chat-model', {'title': title, 'description': description, 'backend_id': backend_id}, this)
        .then((newModel) => {
          this.chatModels.push(newModel);
          this.selectedChatModel = newModel.id;
        });
    },
    retryMessage() {
      //
    },
    openSettingsModal() {
      this.chatSettingsModalIsOpen = true;
    },

    removeChatModel(chatModelId: string, chatModelTitle: string) {
      this.chatModels = this.chatModels.filter((chatModel) => chatModel.id !== chatModelId)
      if (this.selectedChatModel === chatModelId) {
        this.selectedChatModel = "";
      }
      post('/remove-chat-model', {'id': chatModelId}, this);
    },
    updateCurrentAnnotationMessageId(messageId: number) {
      this.currentAnnotationMessageId = messageId;
    },
  },
}
</script>


<style scoped>
#app main {
  overflow-y: hidden;
}

.app-container {
  height: calc(100vh - 200px);
}

.main-container {
  flex-grow: .9; /* take all available space */

  max-width: 100% !important;
  z-index: 0;
}

/* Mobile devices */
@media (max-width: 600px) {
  .main-container {
    width: 100%;
  }
}
</style>
