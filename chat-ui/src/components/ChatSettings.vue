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
              <v-text-field v-model="chat_title" label="Title of Conversation"/>
              <v-text-field v-model="chat_description" label="Description"/>
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
          <v-row v-if="specify_topic"><v-col cols="12"><v-autocomplete label="Dataset of the topic" @update:modelValue="changeDataset" v-model="annotation_dataset" :items="ir_datasets"/></v-col></v-row>
          <v-row v-if="specify_topic"><v-col cols="12"><v-autocomplete label="Topic" v-model="annotation_topic" :items="available_topics" item-title="title" item-value="id"/></v-col></v-row>
          
          <topic-overview :ir_dataset="annotation_dataset" :topic_num="annotation_topic"/>
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
import TopicOverview from "@/components/TopicOverview.vue";

export default {
  props: {
    chatId: {type: String, required: true},
    chatModels: {type: Array, required: true},
    chatIsFinished: {type: Boolean, required: true},
  },
  components: {TopicOverview},
  watch: {
    chatId(newValue) { this.fetchData() }
  },
  computed: {
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
      chat_title: '',
      chat_description: '',
      annotation_dataset: null,
      annotation_topic: null,
      specify_topic: false,
      selectedChatModelErrorMessage: "",
      ir_datasets: ['loading', 'loading'],
      available_topics: [{'id': 1, 'title': 'loading'}, {'id': 2, 'title': 'loading'}],
    }
  },
  beforeMount() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      get('/load-chat/' + this.chatId, this).then(() => 
      get('/api/ir-datasets?id=' + this.annotation_dataset, this))
    },
    closeDialog() {
      this.dialogState = false;
    },
    changeDataset(ir_datasets_id:any) {
      this.available_topics = []
      this.annotation_topic = null
      get('/api/ir-datasets?id=' + ir_datasets_id, this);
    },
    saveChanges() {
      if (this.selectedChatModelState === "") {
        this.selectedChatModelErrorMessage = "Please select a model!";
        return;
      }

      this.$emit('updateChatTitle', this.chat_title);
      this.$emit('updateChatDescription', this.chat_description);
      this.selectedChatModelErrorMessage = "";
      let config = {'chat_title': this.chat_title,
                    'chat_description': this.chat_description,
                    'annotation_dataset': this.annotation_dataset,
                    'annotation_topic': this.annotation_topic,
                   }

      post('/configure-chat/' + this.chatId, config, this).then(() => {this.closeDialog();})
    },
    removeChatModel(id: string, title: string) {
      this.$emit('removeChatModel', id, title);
    },
  },
}
</script>
