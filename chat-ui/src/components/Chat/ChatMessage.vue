<!-- ChatMessage.vue -->
<template>
<v-col cols="12">
    <v-card :class="message.id % 2 === 0 ? 'me-2 rounded-b-shaped': 'ms-2 rounded-e-shaped'">
        <v-toolbar v-if="message.id % 2 === 0"
                   density="compact"
                   color="white"
        >
            <template #prepend>
                <template v-if="message.id % 2 === 0" class="d-flex align-top">
                    <v-avatar
                        class="mr-2"
                        color="white"
                        :image="chatNoirAvatar"></v-avatar>
                    ChatNoir
                </template>
            </template>
            <template #append>
                <v-menu>
                    <template #activator="{ props }">
                        <v-btn
                            v-bind="props"
                            icon="mdi-dots-vertical"
                        >
                        </v-btn>
                    </template>
                    <v-list>
                        <v-list density="compact">
                            <v-list-item @click="() => showExplanationIndices.push(message.id)">
                                <v-list-item-title>Explanation</v-list-item-title>
                            </v-list-item>
                            <v-list-item @click="() => showReferencesIndices.push(message.id)">
                                <v-list-item-title>References</v-list-item-title>
                            </v-list-item>
                        </v-list>
                    </v-list>
                </v-menu>
            </template>
        </v-toolbar>

        <v-toolbar v-if="message.id % 2 === 1"
                   density="compact"
                   color="white"
        >
            <template #append>
                <v-avatar color="#ffffff">
                    <v-img :src="userAvatar"></v-img>
                </v-avatar>
            </template>
        </v-toolbar>

        <v-list-item>
            <v-card-subtitle
            >
                <v-alert
                    v-show="showExplanationIndices.includes(message.id)"

                    border="start"
                    border-color="bg-red-lighten-4"
                    elevation="1"
                >
                    <v-btn
                        small
                        icon
                        variant="text"
                        class="float-right"
                        @click="(e)=> showExplanationIndices.splice(showExplanationIndices.indexOf(message.id), 1)"
                    >
                        <v-icon size="x-small">mdi-close</v-icon>
                    </v-btn>
                    <b>Explanantion</b>
                    <div class="modal-content">
                        <ul>
                            <li><i>Model: </i>test adsf</li>
                            <li><i>Description:</i> test asdf</li>
                            <li><i>Rewritten Message:</i> test afefeg</li>
                        </ul>
                    </div>
                </v-alert>
            </v-card-subtitle>
            <br />
            <v-card-subtitle
            >
                <v-alert
                    v-show="showReferencesIndices.includes(message.id)"

                    border="start"
                    border-color="bg-red-lighten-3"
                    elevation="2"
                >
                    <v-btn
                        small
                        icon
                        variant="text"
                        class="float-right"
                        @click="(e)=> showReferencesIndices.splice(showReferencesIndices.indexOf(message.id), 1)"
                    >
                        <v-icon size="x-small">mdi-close</v-icon>
                    </v-btn>
                    <b>References</b><br />
                    <ul>
                        <li><b>[1] Testwart <br /> <link /></b></li>
                        <li><b>[2] Testwart <br /> <link /></b></li>
                        <li><b>[3] Testwart <br /> <link /></b></li>
                    </ul>
                </v-alert>
            </v-card-subtitle>

            <v-card-text>
                {{ message.text }}
            </v-card-text>
        </v-list-item>
    </v-card>
</v-col>
</template>

<script>
export default {
    // props: ['message', 'chatNoirAvatar', 'userAvatar'],
    props: {
        message: {
            type: Object,
            required: true
        },
        chatNoirAvatar: {
            type: String,
            required: true
        },
        userAvatar: {
            type: String,
            required: true
        }
    },


    data: () => ({
        showExplanationIndices: [0],
        showReferencesIndices: [0]
    })
}
</script>
