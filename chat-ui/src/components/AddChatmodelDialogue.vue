<template>
  <v-dialog v-model="dialogState">
    <v-card>
      <v-card-title>Add new Chatmodel</v-card-title>
      <v-card-text v-if="loading"> <loading :loading="loading"/></v-card-text>
      <v-card-text v-if="!loading">
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="title" label="Name" required/>
              <v-text-field v-model="description" label="Description"/>
            </v-col>
          </v-row>
        </v-container>
        <v-card class="bg-grey-darken-4 ma-4">
          <v-card-title class="bg-grey-darken-3 white--text d-flex justify-space-between">
            <span>Install the ChatNoir Chat Client</span>
          </v-card-title>
          <v-card-text class="language-python overflow-scroll">
            <pre class="language-python pt-4">pip install chatnoir-api</pre>
          </v-card-text>
        </v-card>
        <v-card class="bg-grey-darken-4 ma-4">
          <v-card-title class="bg-grey-darken-3 white--text d-flex justify-space-between">
            <span>Use this code in your application to make your chat modell available</span>
            <v-btn @click="copyToClipboard">Copy</v-btn>
          </v-card-title>
          <v-card-text class="language-python overflow-scroll">
            <pre class="language-python pt-4" v-html="endpointPythonCode" />
          </v-card-text>
        </v-card>
      </v-card-text>
      <v-card-actions class="justify-end">
        <v-btn variant="text" @click="closeDialogue">Close</v-btn>
        <v-btn variant="text" :loading="loading" @click="addChatModel">Add Your ChatModel</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import {get, post} from "@/utils";
import Loading from "../components/Loading.vue"

export default {
  props: {modelValue: Boolean, addNewChatModelFunction: Function},
  components: {Loading},
  emits: ['update:modelValue'],
  data: () => ({
    isDialogueOpen: false,
    title: "",
    description: "",
    loading: true,
    backend_id: ""
  }),
  computed: {
    dialogState: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit('update:modelValue', value);
      }
    },
    endpointPythonCode() {
      let ret = `from chatnoir_api.chat import ChatNoirChatClient

chatnoir = ChatNoirChatClient(`
      if (import.meta.env.DEV) {
        ret += "'ws_host=ws://localhost:8888'"
      }

      ret += `)
chatnoir.serve_chat_backend('`
      
      return ret +  this.backend_id+ "', lambda i: 'You said: ' + i)"
    }
  },
  beforeMount() {
    // TODO: this must be invoked when the user clicks the button, not before...
    //get('/load-add-endpoint-code', this);
  },
  methods: {
    closeDialogue() {
      this.$emit('update:modelValue', false);
    },
    addChatModel() {
      this.addNewChatModelFunction(this.title, this.description, this.backend_id);
      this.title = "";
      this.description = "";
      this.backend_id = "";
      this.closeDialogue();
    },
    copyToClipboard() {
      navigator.clipboard.writeText(this.endpointPythonCode);
    }
  },
  watch: {
    modelValue(newValue) {
      if (newValue === true) {
        this.loading = true;
        this.title = "";
        this.description = "";
        this.backend_id = "";
        post('/api/edit-custom-backend', {}, this)
          .then(() => {this.loading=false})
      }
    }
  }
}
</script>
