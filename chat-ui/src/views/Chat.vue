<template>
  <v-app class="d-flex flex-column app-container">


    <NavigationDrawer v-model="drawerIsOpen"/>
    <loading :loading="loading"/>
    <v-container v-if="!loading" class="main-container w-full pt-0">
      <HeaderToolbar chat-noir-icon="@/assets/img/chanoir-icon.svg"
                     @toggleDrawer="drawerIsOpen = !drawerIsOpen"/>
      <v-row class="pt-2 px-xl-16 d-block text-center">
        <div class="d-flex justify-space-between" v-if="messages.length > 0">
          <v-chip v-if="chatIsFinished" class="ma-2" color="success" variant="outlined" size="large">
            <v-icon start icon="mdi-text"></v-icon>
            Topic: {{ selectedTopic }}
          </v-chip>
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

      <v-row class="px-xl-16" v-for="message in messages" :key="message.id">
        <ChatMessage
            :isSelectable="annotationView === 'utterance'"
            :selectedMessageId="currentAnnotationMessageId"
            :message="message"
            chat-noir-avatar="/assets/img/chatnoir-chat-avatar.svg"
            :user-avatar="user.userAvatar"
            @update:currentAnnotationMessageId="updateCurrentAnnotationMessageId"
        />
      </v-row>
    </v-container>
    <AddChatmodelDialogue v-model="addChatModelModalIsOpen" :addNewChatModelFunction="addNewChatModel"/>
    <ChatSettings :chatTitle="chatTitle"
                  :chatDescription="chatDescription"
                  :chatModels="chatModels"
                  :selectedChatModel="selectedChatModel"
                  :chatIsFinished="chatIsFinished"
                  v-model="chatSettingsModalIsOpen"
                  @updateChatTitle="chatTitle = $event"
                  @updateChatDescription="chatDescription = $event"
                  @updateSelectedChatModel="selectedChatModel = $event"
                  @removeChatModel="removeChatModel"
                  @openAddChatModelDialogue="addChatModelModalIsOpen = true"
    />


    <AssessmentArea v-if="chatIsFinished"
                    :currentAnnotationMessageId="currentAnnotationMessageId"
                    :annotationView="annotationView"
                    :conversationAnnotation="conversationAnnotation"
                    :utteranceAnnotations="utteranceAnnotations"
                    @update:conversationAnnotation="updateConversationAnnotation"
                    @update:annotationView="annotationView = $event"
    />

    <FooterTextarea
        v-model="currentUserMessage"
        v-if="(!loading && !chatIsFinished)"
        :selectedChatModel="selectedChatModelTitle"
        @send-message="sendMessage"
        @retry-message="retryMessage"
        @set-chat-is-finished="setChatisFinished"
        @open-settings-modal="openSettingsModal"


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
import HeaderToolbar from "@/components/HeaderToolbar.vue";
import NavigationDrawer from "@/components/NavigationDrawer.vue";
import {get, post, avatar_src} from "@/utils";
import {ConversationAnnotation, Message, UtteranceAnnotation} from '@/types';
import ChatSettings from "@/components/ChatSettings.vue";


function extractChatIdFromUrl() {
  let loc = ref(window.location).value.href.split('#')[0].split('?')[0]

  if (loc.includes('/cc/')) {
    return loc.split('/cc/')[1].split('/')[0]
  }

  return ''
}

export default {
  components: {
    ChatSettings,
    HeaderToolbar,
    NavigationDrawer,
    AssessmentArea,
    AddChatmodelDialogue,
    ChatMessage,
    FooterTextarea,
    Loading
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
    chatIsFinished: false,
    availableTopics: [' Web Track 2009', 'Obama family tree'],
    selectedTopic: "Obama family tree",
    conversationAnnotation: null as ConversationAnnotation | null,
    utteranceAnnotations: null as UtteranceAnnotation[] | null,
    chatId: extractChatIdFromUrl(),
    chatTitle: "",
    chatDescription: "",
    annotationView: "conversation",
    currentAnnotationMessageId: -1,
  }),
  beforeMount() {
    if ('' + this.chatId === 'undefined' || '' + this.chatId === 'null' || '' + this.chatId === '') {
      get('/load-chat-models', this)
          .then(() => {
            get('/load-chat/new-chat-id', this).then(this.updateUrl)
          });
    } else {
      get('/load-chat-models', this)
          .then(() => {
            get('/load-chat/' + this.chatId, this).then(this.updateUrl)
          });
    }
  },
  methods: {
    setChatisFinished() {
      post('/finish-chat/' + this.chatId, {}, this).then(() => {
        this.chatIsFinished = true
      });
    },
    updateUrl() {
      history.replaceState({'url': '/cc/' + this.chatId}, 'ChatnoirChat', '/cc/' + this.chatId);
      this.chatId = extractChatIdFromUrl();

      if ('' + this.selectedChatModel === '' || '' + this.selectedChatModel === 'undefined' || '' + this.selectedChatModel === 'null') {
        this.selectedChatModel = this.chatModels[0]['id']
      }
    },

    sendMessage() {
      const message: Message = {
        id: this.messages.length, chat_id: this.chatId,
        text: this.currentUserMessage, type: "user", topic: this.selectedTopic,
      }

      post('/send-message/' + this.chatId, {
        'message': this.currentUserMessage,
        'endpoint': this.selectedChatModel
      }, this).then((m) => {
        this.messages.push(message);
        this.currentUserMessage = "";
        this.messages.push(m);
      });
    },
    addNewChatModel(title: string, description: string, backend_id: string) {
      console.log("add new chat model: ", title, description);

      post('/new-chat-model', {'title': title, 'description': description, 'backend_id': backend_id}, this)
          .then((newModel) => {
            console.log("new model: ", newModel)

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
      console.log("remove chat model: ", chatModelId);
      console.log("selectedChatModel: ", this.selectedChatModel);
      if (this.selectedChatModel === chatModelId) {
        this.selectedChatModel = "";
      }
      post('/remove-chat-model', {'id': chatModelId}, this);
    },
    updateConversationAnnotation(updatedAnnotation: ConversationAnnotation) {
      this.conversationAnnotation = updatedAnnotation;
      console.log("Updated conversationAnnotation:", this.conversationAnnotation);
      post('/annotate-chat/' + this.chatId, this.conversationAnnotation, this);
    },
    updateCurrentAnnotationMessageId(messageId: number) {
      console.log("updateCurrentAnnotationMessageId: ", messageId)
      this.currentAnnotationMessageId = messageId;
    },

  },
}
</script>


<style scoped>
.app-container {
  height: calc(100vh - 200px);
}

.main-container {
  flex-grow: 1; /* take all available space */
  overflow-y: auto; /* scroll when content is too much */

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
