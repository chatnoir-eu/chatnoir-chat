<template>
<v-dialog
    :v-model="isDialogueOpen"
>
    <v-card>
        <v-card-title>
            Add new Chatmodel
        </v-card-title>
        <v-card-text>
            <v-container>
                <v-row>
                    <v-col
                        cols="12"
                    >
                        <v-text-field
                            label="Name"
                            required
                        ></v-text-field>

                        <v-text-field
                            label="Description"
                        ></v-text-field>
                    </v-col>
                </v-row>
            </v-container>
            <v-card class="bg-grey-darken-4">
                <v-card-title class="bg-grey-darken-3 white--text d-flex justify-space-between">
                    <span>Use this code in your application to make your chat modell available</span>
                    <v-btn @click="copyToClipboard">Copy</v-btn>
                </v-card-title>
                <v-card-text class="language-python overflow-scroll">
                    <pre class="language-python pt-4">
                        class BasicUIMeta(metaclass=abc.ABCMeta):
                          @abc.abstractmethod
                          def click(self, x: int, y: int):
                            pass

                          @abc.abstractmethod
                            def swipe(self, fx: int, fy: int, tx: int, ty: int, duration: float):
                              """ duration is float type, indicate seconds """

                          @abc.abstractmethod
                            def window_size(self) -> tuple:
                              """ return (width, height) """
                    </pre>
                </v-card-text>
            </v-card>
        </v-card-text>
        <v-card-actions class="justify-end">
            <v-btn
                variant="text"
                @click="addChatModel"
            >
                Add
            </v-btn>
            <v-btn
                variant="text"
                @click="closeDialogue"
            >
                Close
            </v-btn>
        </v-card-actions>
    </v-card>
</v-dialog>
</template>
<script>
export default {
    props: {
        isOpen: {
            type: Boolean,
            default: false
        }
    },
    emits: ['update:isOpen'],
    data: () => ({
        isDialogueOpen: false,
        endpointPythonCode:
            `class BasicUIMeta(metaclass=abc.ABCMeta):
          @abc.abstractmethod
          def click(self, x: int, y: int):
              pass

          @abc.abstractmethod
          def swipe(self, fx: int, fy: int, tx: int, ty: int, duration: float):
              """ duration is float type, indicate seconds """

          @abc.abstractmethod
          def window_size(self) -> tuple:
              """ return (width, height) """
        `
    }),
    watch: {
        isOpen(newValue) {
            this.isDialogueOpen = newValue;
        }
    },
    methods: {
        closeDialogue() {
            this.$emit('update:isOpen', false);
        },
        addChatModel(){
            //TODO: add request to endpoint

            this.closeDialogue();
        },
        copyToClipboard() {
            navigator.clipboard.writeText(this.endpointPythonCode);
        }
    },
}
</script>