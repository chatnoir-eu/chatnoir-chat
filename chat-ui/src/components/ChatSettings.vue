<template>
  <v-dialog v-model="dialogState">
    <v-card>
      <v-card-title>
        <v-icon>mdi-cog</v-icon>
        Chat Settings
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="localTitle" label="Title of Conversation"/>
              <v-text-field v-model="localDescription" label="Description"/>
              <v-select v-if="!chatIsFinished" label="Select Chatmodel" v-model="selectedChatModelState" :items="chatModels" item-title="title" item-value="id" :error-messages="selectedChatModelErrorMessage">
                <template v-slot:item="{ props, item }">
                  <v-list-item v-bind="props" :subtitle="item.raw.isRemovable">
                    <template v-slot:append>
                      <v-btn variant="text" v-if="item.raw.isRemovable" icon :onclick="() => removeChatModel(item.raw.id, item.raw.title)">
                        <v-icon>mdi-trash-can-outline</v-icon>
                      </v-btn>
                    </template>
                  </v-list-item>
                </template>
                <template #append>
                  <v-btn @click="$emit('openAddChatModelDialogue')">
                    <v-icon>mdi-plus</v-icon>
                  </v-btn>
                </template>
              </v-select>
            </v-col>
          </v-row>

          <v-row><v-col cols="12"><v-switch label="Specify an Topic" v-model="specify_topic"/></v-col></v-row>
          <v-row v-if="specify_topic"><v-col cols="12"><v-autocomplete label="Dataset of the topic" @update:modelValue="changeDataset" v-model="topic_dataset" :items="ir_datasets"/></v-col></v-row>
          <v-row v-if="specify_topic"><v-col cols="12"><v-autocomplete label="Topic" @update:modelValue="changeTopic" v-model="topic_topic" :items="available_topics" item-title="title" item-value="id"/></v-col></v-row>
          <v-row v-if="show_details"><v-col cols="12"><v-text-field label="Description" disabled v-model="topic_details['description']"/></v-col></v-row>
          <v-row v-if="show_details"><v-col cols="12"><v-text-field label="Narrative" disabled v-model="topic_details['narrative']"/></v-col></v-row>
        </v-container>
      </v-card-text>
      <v-card-actions class="justify-end">
        <v-btn @click="closeDialog">Cancel</v-btn>
        <v-btn @click="saveChanges">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>


<script lang="ts">
import { post, get } from '@/utils'

export default {
  props: {
    chatTitle: {type: String, required: true},
    chatDescription: {type: String, required: true},
    modelValue: {type: Boolean, default: false},
    selectedChatModel: {type: String, required: true},
    chatModels: {type: Array, required: true},
    chatIsFinished: {type: Boolean, required: true},
    chatId: {type: String, required: true},
  },

  watch: {
    modelValue(newValue) {
      if (newValue) { // if dialog is being opened, reset the values to the values from the parent component
        this.localTitle = this.chatTitle;
        this.localDescription = this.chatDescription;
        this.localSelectedChatModel = this.selectedChatModel;
      }
    }
  },

  computed: {
    show_details() {
      return this.topic_details && this.topic_details['description'] + '' !== 'null' && this.topic_details['description'] + '' !== 'loading' && this.topic_details['description'] + '' !== 'undefined';
    },
    dialogState: {
      get() {
        return this.modelValue;
      },
      set(value: string) {
        this.$emit('update:modelValue', value);
      }
    },
    selectedChatModelState: {
      get() {
        return this.selectedChatModel;
      },
      set(value: string) {
        this.$emit('updateSelectedChatModel', value);
      }
    }
  },
  emits: ['removeChatModel','updateChatTitle', 'updateChatDescription', 'update:modelValue', 'updateSelectedChatModel', 'openAddChatModelDialogue'],
  data() {
    return {
      localTitle: this.chatTitle,
      localDescription: this.chatDescription,
      localSelectedChatModel: this.selectedChatModel,
      selectedChatModelErrorMessage: "",
      specify_topic: false,
      topic_dataset: null,
      ir_datasets: ['loading', 'loading'],
      available_topics: [{'id': 1, 'title': 'loading'}, {'id': 2, 'title': 'loading'}],
      topic_topic: null,
      topic_details: {'title': 'loading', 'description': 'loading', 'narrative': 'loading'}
    }
  },
  beforeMount() {
    get('/api/ir-datasets', this);
  },
  methods: {
    closeDialog() {
      this.dialogState = false;
    },
    changeDataset(ir_datasets_id:any) {
      this.available_topics = []
      this.topic_topic = null
      this.topic_details = {'title': 'loading', 'description': 'loading', 'narrative': 'loading'}
      get('/api/ir-datasets?id=' + ir_datasets_id, this);
    },
    changeTopic(topic_id: any) {
      this.topic_details = {'title': 'loading', 'description': 'loading', 'narrative': 'loading'}
      get('/api/ir-datasets?id=' + this.topic_dataset + '&topic_id=' + topic_id, this);
    },
    saveChanges() {
      if (this.selectedChatModelState === "") {
        this.selectedChatModelErrorMessage = "Please select a model!";
        return;
      }

      this.$emit('updateChatTitle', this.localTitle);
      this.$emit('updateChatDescription', this.localDescription);
      this.selectedChatModelErrorMessage = "";
      let config = {'chat_title': this.localTitle,
                    'chat_description': this.localDescription,
                    'annotation_dataset': this.topic_dataset,
                    'annotation_topic': this.topic_topic,
                   }

      post('/configure-chat/' + this.chatId, config, this).then(() => {this.closeDialog();})
    },
    removeChatModel(id: string, title: string) {
      this.$emit('removeChatModel', id, title);
    },
  },
}
</script>
