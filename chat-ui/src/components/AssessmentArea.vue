<template>
  <div class="fixed-input">
    <v-divider
      thickness="4"
      color="black"
    >
    </v-divider>

    <v-card>
      <h3 class="text-center">Assessment Area</h3>
      <v-tabs
        v-model="localAnnotationView"
        color="red"
        align-tabs="center"
      >
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
                  <v-radio-group
                    class="d-inline-block"
                    v-model="conversationAnswers[index]"
                    inline
                  >
                    <v-radio
                      label="Yes"
                      value="Yes"
                    ></v-radio>
                    <v-radio
                      label="No"
                      value="No"
                    ></v-radio>
                  </v-radio-group>

                </div>
                <v-divider
                  v-if="index !== conversationAnnotation.length -1"
                  thickness="2"
                  color="black"
                  :key="index"
                  class="my-4"
                ></v-divider>
              </div>


            </div>

          </v-window-item>

          <v-window-item class="text-center" value="utterance">
            Click on an utterance to start annotating it. [NOT WORKING YET]
          </v-window-item>
        </v-window>
      </v-card-text>
    </v-card>

  </div>
</template>


<script lang="ts">
import {ConversationAnnotation, UtteranceAnnotation} from '@/types';

export default {
  props: {
    annotationView: {
      type: String,
      required: true
    },
    conversationAnnotation: {
      type: Object as () => ConversationAnnotation | null,
      required: true
    },
    utteranceAnnotations: {
      type: Array as () => UtteranceAnnotation[] | null,
      required: true
    },
    currentAnnotationMessageId: {
      type: number,
      required: true
    }
  },
  emits: ['update:conversationAnnotation', 'update:annotationView', 'update:utteranceAnnotations'],

  data() {
    return {
      localInput: this.modelValue,
      localAnnotationView: this.annotationView,
      conversationAnswers: [] as (string | null)[],
      // utteranceAnswers: [],
    };
  },
  computed: {
    currentUtteranceAnnotation() {
      if (this.currentAnnotationMessageId === -1) {
        return null;
      }
      return this.utteranceAnnotations ? this.utteranceAnnotations[this.currentAnnotationMessageId] : null;
    }
  },
  watch: {
    conversationAnnotation: {
      deep: true,
      handler() {
        this.$emit('update:conversationAnnotation', this.conversationAnnotation);
      }
    },
    // utteranceAnnotations: {
    //   deep: true,
    //   handler() {
    //     this.$emit('update:utteranceAnnotations', this.utteranceAnnotations);
    //   }
    // },

    localAnnotationView(newValue) {
      this.$emit('update:annotationView', newValue);
    },
    conversationAnswers: {
      deep: true,
      handler() {
        // Merge questions and answers, then emit
        if (!this.conversationAnnotation) {
          return;
        }
        const updatedAnnotation = this.conversationAnnotation.map((q, index) => ({
            ...q,
            answer: this.conversationAnswers[index]
        }));
        this.$emit('update:conversationAnnotation', updatedAnnotation);
      }
    },
  },
  mounted() {
    if (this.conversationAnnotation !== null) {
      console.log(this.conversationAnnotation);
      console.log("mounted");
      this.conversationAnswers = this.conversationAnnotation.map(q => q.answer || null);
    }
    // Similar initialization for utteranceAnnotations
  },

  methods: {},
};
</script>
<style scoped>
.fixed-input {

  width: 100%;
  z-index:0; /* Make sure it's above the chat messages */
  padding: 0 16px; /* Some padding, adjust as needed */
  background-color: white; /* Background color to cover messages underneath */
}

</style>
