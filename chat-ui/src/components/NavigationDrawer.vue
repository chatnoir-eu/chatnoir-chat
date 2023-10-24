<!-- NavigationDrawer.vue -->
<template>
  <v-navigation-drawer :value="drawerValue" temporary location="right" @input="handleDrawerInput">
    <v-list-item :prepend-avatar="user.userAvatar" :title="user.userName"
    ></v-list-item>

    <v-divider></v-divider>

    <v-list density="compact" nav>
      <v-list-item href="/" prepend-icon="mdi-plus" title="New Chat" value="home"></v-list-item>
      <v-divider></v-divider>
      <v-list-subheader>Your History</v-list-subheader>

      <v-list-item :href="chat.link" :title="chat.title" v-for="chat in chatHistory" :key="chat.link" prepend-icon="mdi-chat">
      </v-list-item>

    </v-list>
  </v-navigation-drawer>
</template>

<script>
import {get, avatar_src} from "@/utils";
import ChatMessage from "@/components/ChatMessage.vue";

export default {
  components: {ChatMessage},
  props: {
    drawerValue: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    chatHistory: [{link: '/cc/1', title: 'Test chat'}],
    user: avatar_src()
  }),
  beforeMount() {
    get('/load-chat-history', this);
  },
  emits: ['update:drawerValue'],
  methods: {
    handleDrawerInput(newValue) {
      this.$emit('update:drawerValue', newValue);
    }
  }
}
</script>
