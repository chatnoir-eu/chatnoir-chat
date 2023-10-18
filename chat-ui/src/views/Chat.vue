<!-- ParentComponent.vue or whatever your main component's name is -->
<template>
<v-app ref="app" class="app-layout">
    <HeaderToolbar :chat-noir-icon="chatNoirIcon" @toggleDrawer="drawer = !drawer" />
    <NavigationDrawer v-model="drawer" />
    <v-container class="main-container">
        <v-main class="main-content">
            <v-container>
                <v-row>
                    <v-select
                        v-model="selectedChatModel"
                        class="py-5"
                        :items="items"
                        :item-title="item => item.title"
                        :item-value="item => item.isRemovable"
                        dense
                        variant="outlined"
                        label="Select your Chatmodel"
                    >
                        <template #item="{ item, props }">
                            <v-list-item
                                v-bind="props"
                                :title="item.title"
                            >
                                <template #append>
                                    <v-btn v-if="item.value" icon>
                                        <v-icon>mdi-trash-can-outline</v-icon>
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

                <v-row v-for="message in messages" :key="message.id">
                    <ChatMessage :message="message" :chat-noir-avatar="chatNoirAvatar" :user-avatar="userAvatar" />
                </v-row>
                <v-row>
                </v-row>
            </v-container>
        </v-main>
    </v-container>
    <AddChatmodelDialogue v-model="addChatModelDialogueIsOpen" />

    <FooterTextarea v-model="currentUserMessage"
                    @send-message="sendMessage"
                    @retry-message="retryMessage" />
</v-app>
</template>


<script>

import HeaderToolbar from "@/components/Chat/HeaderToolbar.vue";
import NavigationDrawer from "@/components/Chat/NavigationDrawer.vue";
import ChatMessage from "@/components/Chat/ChatMessage.vue";
import FooterTextarea from "@/components/Chat/FooterTextarea.vue";
import AddChatmodelDialogue from "@/components/Chat/AddChatmodelDialogue.vue";

export default {
    components: {
        AddChatmodelDialogue,
        HeaderToolbar,
        NavigationDrawer,
        ChatMessage,
        FooterTextarea
    },
    data: () => ({
        selected_tags: [],
        addChatModelDialogueIsOpen: false,
        messages: [{id: 0, text: "Hello World"},
                   {id: 1, text: "Hello World 2"},
                   {id: 2, text: "Hello World 3"},
                   {id: 3, text: "jasldkf"},
                   {id: 4, text: "Hello World 4"},
                   {id: 5, text: "Hello World 5"},
                   {id: 6, text: "Hello World 6"},
                   {id: 7, text: "Hello World 7"},
                   {id: 8, text: "Hello World 8"},
                   {id: 9, text: "Hello World 9"},
                   {id: 10, text: "Hello World 10"},
                   {id: 11, text: "Hello World 11"},
                   {id: 12, text: "Hello World 12"},
                   {id: 13, text: "Hello World 13"},
                   {id: 14, text: "orem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."},
                   {id: 15, text: "Hello World 15Hello World 15Hello World 15Hello World 15Hello World 15Hello World 15Hello World 15Hello World 15Hello World 15" +
                       "Hello World 15Hello World 15Hello World 15Hello World 15Hello World 15Hello World 15Hello World 15"},
        ],
        chatNoirAvatar: require('@/assets/img/chatnoir-chat-avatar.svg'),
        chatNoirIcon: require('@/assets/img/chatnoir-icon.svg'),
        userAvatar: "https://randomuser.me/api/portraits/men/78.jpg",
        drawer: false,
        selectedChatModel: null,
        items: [
            {title: 'Chat Model asjkfldö', isRemovable: true},
            {title: 'Chat Model 2', isRemovable: false},
            {title: 'Chat Model 3', isRemovable: true},
        ],
        currentUserMessage: "",

    }),

    methods: {
        sendMessage() {
            this.messages.push({id: this.messages.length, text: this.currentUserMessage});
            this.currentUserMessage = "";
        },
        retryMessage() {
            //
        },
        addNewChatModel() {
        // Handle logic for adding a new chat model
        },
        removeChatModel(chatModel) {
        // Handle logic for removing the specified chat model
        },
    },
}
</script>


<style scoped>

.app-layout {
  display: flex;
  flex-direction: column; /* children are stacked vertically */
  height: 100vh;
}

.main-content {
  flex-grow: 1; /* take all available space */
  overflow-y: auto; /* scroll when content is too much */
}

.main-container {
    width: 75%;
    margin: 0 auto;  /* to center the container */
}

/* Mobile devices */
@media (max-width: 600px) {
    .main-container {
        width: 100%;
    }
}


</style>
