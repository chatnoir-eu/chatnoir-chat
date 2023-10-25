<template>
  <v-toolbar elevation="4">
    <v-toolbar-title>
      <v-avatar class="mr-2" color="white" image="../assets/img/chatnoir-icon.svg"/>
    </v-toolbar-title>

    <v-btn class="ma-2" icon @click.stop="$emit('toggleDrawer')">
      <v-icon>mdi-menu</v-icon>
    </v-btn>
  </v-toolbar>
</template>

<script>
export default {
  props: ['chatNoirIcon'],
  emits: ['toggleDrawer'],
  data: () => ({})
}
</script>
