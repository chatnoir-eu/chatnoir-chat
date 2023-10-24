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
        v-model="tab"
        color="red"
        align-tabs="center"
      >
        <v-tab value="one">Conversation</v-tab>
        <v-tab value="two">Single Utterance</v-tab>
      </v-tabs>

      <v-card-text>
        <v-window v-model="tab">
          <v-window-item class="text-center" value="one">
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

          <v-window-item class="text-center" value="two">
            Click on an utterance to start annotating it. [NOT WORKING YET]
          </v-window-item>
        </v-window>
      </v-card-text>
    </v-card>

  </div>
</template>


<script lang="ts">
import {ConversationAnnotation} from '@/types';

export default {
  props: {
    conversationAnnotation: {
      type: Object as () => ConversationAnnotation | null,
      required: true
    },
    // utteranceAnnotations: {
    //   type: Array as () => UtteranceAnnotation[] | null,
    //   required: true
    // }
  },
  // emits: ['update:conversationAnnotation', 'update:utteranceAnnotations'],
  emits: ['update:conversationAnnotation'],

  data() {
    return {
      localInput: this.modelValue,
      tab: "one",
      conversationAnswers: [] as (string | null)[],
      // utteranceAnswers: [],
    };
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
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  max-height: 50vh;
  z-index: 2; /* Make sure it's above the chat messages */
  padding: 1em 1em; /* Some padding, adjust as needed */
  margin-top: 8em;
  background-color: white; /* Background color to cover messages underneath */
}

</style>
