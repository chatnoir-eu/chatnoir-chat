<template>
  <div class="fixed-input">
    <v-divider thickness="4" color="black">
    </v-divider>
    <v-card>
      <h3 class="text-center">Assessment Area</h3>
      <v-tabs v-model="localAnnotationView" color="red" align-tabs="center">
        <v-tab value="conversation">Conversation</v-tab>
        <v-tab value="utterance">Single Utterance</v-tab>
      </v-tabs>
      <v-card-text>
        <v-window v-model="localAnnotationView">
          <v-window-item class="text-center" value="conversation">
            <div v-if="conversationAnnotation">
              <div v-for="(question, index) in conversationAnnotation" :key="question.question_id">
                <div class="d-inline text-center" v-if="question.response_type === 'Yes/No'">
                  <h4>{{ question.question_text }}</h4>
                  <v-radio-group class="d-inline-block" v-model="conversationAnswers[index]" inline>
                    <v-radio label="Yes" value="Yes"/>
                    <v-radio label="No" value="No"/>
                  </v-radio-group>
                </div>

                <div class="d-inline text-center" v-if="question.response_type === 'Likert'">
                  <h4>{{ question.question_text }}</h4>
                  <v-radio-group class="d-inline-block" v-model="conversationAnswers[index]" inline>
                    <v-radio label="1" value="1"/>
                    <v-radio label="2" value="2"/>
                    <v-radio label="3" value="3"/>
                    <v-radio label="4" value="4"/>
                    <v-radio label="5" value="5"/>
                  </v-radio-group>
                </div>

                <div class="d-inline text-center" v-if="question.response_type === 'Text'">
                  <h4>{{ question.question_text }}</h4>
                  <v-textarea class="px-xl-16 mt-4" v-model="conversationAnswers[index]" hide-details auto-grow rows="2" max-rows="5" variant="outlined"/>
                </div>

                <v-divider v-if="index !== conversationAnnotation.length -1" thickness="2" color="black" :key="index" class="my-4"/>
              </div>
            </div>
          </v-window-item>
          <v-window-item class="text-center" value="utterance">
            <div v-if="selectedMessageId < 0">Please select an Utterance.</div>
            <div v-if="selectedUtteranceAnnotation === null && selectedMessageId >= 0">No questions available. Contact Admin.</div>
            <div v-if="selectedUtteranceAnnotation">
              <div v-for="(question, index) in selectedUtteranceAnnotation.questions"
                   :key="question.question_id">
                <div class="d-inline text-center" v-if="question.response_type === 'Yes/No'">
                  <h4>{{ question.question_text }}</h4>
                  <v-radio-group class="d-inline-block" v-model="selectedUtteranceAnswers[index]" inline>
                    <v-radio label="Yes" value="Yes"/>
                    <v-radio label="No" value="No"/>
                  </v-radio-group>
                </div>
                <v-divider v-if="index !== selectedUtteranceAnnotation.questions.length - 1" thickness="2" color="black" :key="index" class="my-4"/>
              </div>
            </div>
          </v-window-item>
        </v-window>
        <div class="d-flex justify-space-between px-xl-16 my-2 " style="font-size: .7em;">
          <v-btn class="my-2" variant="tonal" size="x-small" @click="$emit('toggle-drawer')">
            <v-icon>mdi-history</v-icon>
            History
          </v-btn>
        </div>

      </v-card-text>
    </v-card>

  </div>
</template>


<script lang="ts">
import {ConversationAnnotation, UtteranceAnnotation} from '@/types';
import { post, get } from '@/utils'

export default {
  props: {
    annotationView: {type: String, required: true},
    selectedMessageId: {type: Number, required: true},
    chatId: {type: String, required: true}
  },
  emits: ['update:annotationView', 'toggle-drawer'],
  data() {
    return {
      localInput: this.modelValue,
      localAnnotationView: this.annotationView,
      conversationAnswers: [] as (string | null)[],
      selectedUtteranceAnswers: [] as (string | null)[],
      conversationAnnotation: [] as ConversationAnnotation | null,
      utteranceAnnotations: [] as UtteranceAnnotation[] | null,
    };
  },
  computed: {
    selectedUtteranceAnnotation() {
      if (this.selectedMessageId === -1 || this.utteranceAnnotations === null) {
        return null;
      }

      return this.utteranceAnnotations;
    }
  },
  watch: {
    selectedMessageId(newId, oldId) {
      if (newId !== oldId && this.utteranceAnnotations !== null) {
        const selectedUtterance = this.utteranceAnnotations.find(UA => UA.utterance_id === newId);
        if (selectedUtterance) {
          this.selectedUtteranceAnswers = selectedUtterance.questions.map(q => q.answer || null);
        }
      }
    },
    localAnnotationView(newValue) {
      this.$emit('update:annotationView', newValue);
    },
    selectedUtteranceAnswers: {
      deep: true,
      handler() {
        if (!this.selectedUtteranceAnnotation) {
          return;
        }
        const updatedAnnotation = {
          ...this.selectedUtteranceAnnotation,
          questions: this.selectedUtteranceAnnotation.questions.map((q, index) => ({
            ...q,
            answer: this.selectedUtteranceAnswers[index]
          }))
        };
        const updatedUtteranceAnnotations = this.utteranceAnnotations?.map(ua => ua.utterance_id === updatedAnnotation.utterance_id ? updatedAnnotation : ua);

        this.$emit('update:utteranceAnnotations', updatedUtteranceAnnotations);
      }
    },
  },
  beforeMount() {
    get('/api/annotations-for-chat/' + this.chatId, this);
  },
  methods: {},
};
</script>
<style scoped>
.fixed-input {

  width: 100%;
  z-index: 0; /* Make sure it's above the chat messages */
  padding: 0 16px; /* Some padding, adjust as needed */
  background-color: white; /* Background color to cover messages underneath */
}

</style>
