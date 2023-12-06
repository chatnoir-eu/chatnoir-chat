<template>
  <v-chip class="ma-2" color="success" variant="outlined" size="large">
    <v-icon start icon="mdi-text"/>
      Topic: {{ selectedTopic }}
  </v-chip>
  <v-row ><v-col cols="12"><v-text-field label="Description" disabled v-model="topic_details['description']"/></v-col></v-row>
          <v-row v-if="show_details"><v-col cols="12"><v-text-field label="Narrative" disabled v-model="topic_details['narrative']"/></v-col></v-row>
</template>

<script lang="ts">
export default {
  name: "topic-overview",
  props: ['ir_dataset', 'topic_num'],
  watch: {
    ir_dataset(newValue) { this.fetchData() },
    topic_num(newValue) { this.fetchData() }
  },
  methods: {
    fetchData() {
      this.dialogState = false;
    },
  },
  beforeMount() {
    fetchData();
  }
}
</script>
