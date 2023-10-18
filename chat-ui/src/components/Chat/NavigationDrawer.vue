<!-- NavigationDrawer.vue -->
<template>
<v-navigation-drawer :value="drawerValue" temporary location="right" @input="handleDrawerInput">
    <v-list-item
        prepend-avatar="https://randomuser.me/api/portraits/men/78.jpg"
        title="Unknown user"
    ></v-list-item>

    <v-divider></v-divider>

    <v-list density="compact" nav>
        <v-list-item prepend-icon="mdi-plus" title="New Chat" value="home"></v-list-item>
        <v-divider></v-divider>
        <v-list-subheader>Your History</v-list-subheader>
        <v-list-item prepend-icon="mdi-chat" title="2023-08-12.12:48:02" value="about"></v-list-item>
        <v-list-item prepend-icon="mdi-chat" title="2023-08-12.12:48:02" value="about"></v-list-item>
    </v-list>
</v-navigation-drawer>
</template>

<script>
export default {
    props: {
        drawerValue: {
            type: Boolean,
            default: false
        }
    },
    emits: ['update:drawerValue'],
    methods: {
        handleDrawerInput(newValue) {
            this.$emit('update:drawerValue', newValue);
        }
    }
}
</script>
