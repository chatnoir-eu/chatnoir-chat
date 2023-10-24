<template>
  <v-dialog v-model="dialogState">
    <v-card>
      <v-card-title>
        <v-icon>mdi-cog</v-icon>
        Chat Settings
      </v-card-title>
      <v-card-text v-if="loading">
        <loading :loading="loading"/>
      </v-card-text>
      <v-card-text v-if="!loading">
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="title" label="Title of Conversation"/>
              <v-text-field v-model="description" label="Description"/>
              <v-select v-if="!chatIsFinished"
                        label="Select Chatmodel"
                        v-model="selectedChatModel"
                        :items="chatModels"
                        item-title="title"
                        item-value="id">
                <template v-slot:item="{ props, item }">
                  <v-list-item
                    v-bind="props"
                    :subtitle="item.raw.isRemovable">
                    <template v-slot:append>
                      <v-btn
                        variant="text"
                        v-if="item.raw.isRemovable"
                        icon
                        :onclick="() => removeChatModelFunction(item.raw.id, item.raw.title)">
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

            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions class="justify-end">
        <v-btn variant="text" @click="closeDialogue">
          <v-icon>mdi-close</v-icon>
          Cancel
        </v-btn>
        <v-btn variant="text" :loading="loading" @click="addChatModel">
          <v-icon>mdi-check</v-icon>
          save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import {get, post} from "@/utils";
import Loading from "../components/Loading.vue"
import {ChatModel} from "@/types";

export default {
  props: {
    modelValue: Boolean,
    addNewChatModelFunction: Function,
    removeChatModelFunction: Function,
    selectChatModelFunction: Function,
    chatIsFinished: Boolean,
    chatModels: [] as ChatModel[],
    selectedChatModel: Object

  },
  components: {Loading},
  emits: ['update:modelValue'],
  data: () => ({
    modalIsOpen: false,
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

      return ret + this.backend_id + "', lambda i: 'You said: ' + i)"
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
          .then(() => {
            this.loading = false
          })
      }
    }
  }
}
</script>
