<template>
<v-toolbar :elevation="8">
    <v-toolbar-title>
        <v-avatar :image="chatNoirIcon"></v-avatar>
    </v-toolbar-title>

    <v-text-field
        class="my-6"
        variant="filled"
        color="#ca4525"
        label="Title of Conversation"
        hide-details="true"
        density="compact"
    ></v-text-field>

    <v-btn class="ma-2" icon @click.stop="$emit('toggleDrawer')">
        <v-icon>mdi-menu</v-icon>
    </v-btn>
</v-toolbar>
</template>

<script>
export default {
    props: ['chatNoirIcon'],
    emits: ['toggleDrawer'],
    data: () => ({
    
    })
}
</script>
