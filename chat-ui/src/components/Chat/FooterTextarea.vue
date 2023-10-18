<template>
<v-divider
    :thickness="3"
    class="border-opacity-100 py-9"
    color="black"
></v-divider>
<v-container :elevation="8" class="fixed-bottom-container">
    <v-lazy>
        <v-textarea
            :value="localInput"
            hide-details
            placeholder="Type your message here"
            auto-grow
            rows="1"
            max-rows="3"
            variant="solo"
            @input="handleInput"
        >
            <template #append>
                <v-btn v-if="modelValue.trim().length > 0" variant="text" icon @click.stop="emitSendMessage">
                    <v-icon>mdi-send</v-icon>
                </v-btn>
                <v-btn v-else variant="text" icon @click.stop="emitRetryMessage">
                    <v-icon>mdi-reload</v-icon>
                </v-btn>
            </template>
        </v-textarea>
    </v-lazy>
</v-container>
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
.fixed-bottom-container {
  position: sticky;
  bottom: 0;
  background: white;
}

</style>