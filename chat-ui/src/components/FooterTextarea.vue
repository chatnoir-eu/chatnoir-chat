<template>
  <div class="fixed-input">
    <v-divider :thickness="1" color="black"></v-divider>
    <v-textarea class="px-xl-16 mt-4" v-model="localInput" hide-details placeholder="Type your message here"
                auto-grow rows="1" max-rows="3" variant="outlined"
                @keydown.enter="checkForEnter($event)"
    >
      <template #append-inner>
        <v-btn v-if="modelValue.trim().length > 0" variant="text" icon @click="emitSendMessage">
          <v-icon>mdi-send</v-icon>
        </v-btn>
        <v-btn v-else variant="text" icon @click.stop="emitRetryMessage">
          <v-icon>mdi-reload</v-icon>
        </v-btn>
      </template>
    </v-textarea>

    <div class="d-flex justify-space-between px-xl-16 my-2 " style="font-size: .7em;">
      <span>Model: {{ selectedChatModel }}</span>
      <div>
        <v-btn class="my-2" variant="tonal" size="x-small" @click="emitSetChatIsFinished">
          <v-icon>mdi-cog</v-icon>
          Annotate
        </v-btn>
        <v-btn class="my-2" variant="tonal" size="x-small" @click="emitOpenSettingsModal">
          <v-icon>mdi-cog</v-icon>
          Settings
        </v-btn>
        <v-btn class="my-2" variant="tonal" size="x-small" @click="emitToggleDrawer">
          <v-icon>mdi-history</v-icon>
          History
        </v-btn>
      </div>
    </div>
  </div>
</template>


<script lang="ts">
export default {
  props: {
    modelValue: {
      type: String,
      required: true
    },
    selectedChatModel: {
      type: String,
      required: true
    },
  },
  emits: ['update:modelValue', 'send-message', 'retry-message', 'set-chat-is-finished', 'open-settings-modal', 'toggle-drawer'],
  data() {
    return {
      localInput: this.modelValue
    };
  },
  computed: {
    isMobile() {
      return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    }
  },
  watch: {
    modelValue(newValue) {
      this.localInput = newValue;
    },
    localInput(newValue) {
      this.$emit('update:modelValue', newValue);
    }
  },
  methods: {
    emitSendMessage() {
      this.$emit('send-message');
    },
    emitRetryMessage() {
      this.$emit('retry-message');
    },
    emitSetChatIsFinished() {
      this.$emit('set-chat-is-finished');
    },
    emitOpenSettingsModal() {
      this.$emit('open-settings-modal');
    },
    emitToggleDrawer() {
      this.$emit('toggle-drawer');
    },
    checkForEnter(event: KeyboardEvent) {
    // Prevent default action when both Shift and Enter are pressed (Shift+Enter = new line). Otherwise, send message.
      if (event.shiftKey || this.isMobile) {
        return;
      }
      this.emitSendMessage();
    },

  }
}
</script>
<style scoped>
.fixed-input {

  width: 100%;
  z-index: 0; /* Make sure it's above the chat messages */
  padding: 0 16px; /* Some padding, adjust as needed */
  background-color: white; /* Background color to cover messages underneath */
}

</style>
