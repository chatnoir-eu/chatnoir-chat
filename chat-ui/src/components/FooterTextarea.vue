<template>
  <div class="fixed-input">
    <v-divider :thickness="1" color="black"></v-divider>
    <v-textarea class="px-xl-16 mt-4" :value="localInput" hide-details placeholder="Type your message here"
                auto-grow rows="1" max-rows="3" variant="outlined" @input="handleInput">
      <template #append>
        <v-btn v-if="modelValue.trim().length > 0" variant="text" icon @click.stop="emitSendMessage">
          <v-icon>mdi-send</v-icon>
        </v-btn>
        <v-btn v-else variant="text" icon @click.stop="emitRetryMessage">
          <v-icon>mdi-reload</v-icon>
        </v-btn>
      </template>
    </v-textarea>
    <p class="mb-3 font-weight-thin" style="font-size: .7em;">Model: tbd (<a href="">Settings</a>). <a href="">Annotate chat</a>.</p>
  </div>
</template>


<script>
export default {
  props: {
    modelValue: {
      type: String,
      required: true
    }
  },
  emits: ['update:modelValue', 'send-message', 'retry-message'],
  data() {
    return {
      localInput: this.modelValue
    };
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
    handleInput(event) {
      this.localInput = event.target.value;
    },
    emitSendMessage() {
      this.$emit('send-message');
    },
    emitRetryMessage() {
      this.$emit('retry-message');
    },
  }
}
</script>
<style scoped>
.fixed-input {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  z-index: 2; /* Make sure it's above the chat messages */
  padding: 0 16px; /* Some padding, adjust as needed */
  background-color: white; /* Background color to cover messages underneath */
}

</style>
