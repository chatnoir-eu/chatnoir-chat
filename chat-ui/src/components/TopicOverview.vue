<template>
  <span v-if="show_topic">
    <v-chip class="ma-2" color="success" variant="outlined" size="large" @click="expanded = !expanded">
      <v-icon start icon="mdi-text"/>
      Topic: {{ title }}
      <v-icon v-if="!expanded" end icon="mdi-plus"/>
      <v-icon v-if="expanded" end icon="mdi-minus"/>
    </v-chip>
    <div v-if="expanded">
      <v-row><v-col cols="12"><v-textarea label="Description" disabled hide-details auto-grow rows="2" max-rows="5" v-model="description"/></v-col></v-row>
      <v-row><v-col cols="12"><v-textarea label="Narrative" disabled  hide-details auto-grow rows="2" max-rows="5" v-model="narrative"/></v-col></v-row>

      <v-data-table :items="qrels" :items-per-page="5">
        <template #item.Document="{ item }">
          <a target="_blank" :href="'/datasets/docs?ir_dataset_id=' + ir_dataset + '&doc_id=' + item['Document']">{{ item["Document"] }}</a>
        </template>
      </v-data-table>
    </div>
  </span>
</template>

<script lang="ts">
import { get } from '@/utils'

export default {
  name: "topic-overview",
  props: ['ir_dataset', 'topic_num'],
  watch: {
    ir_dataset(newValue) { this.fetchData() },
    topic_num(newValue) { this.fetchData() }
  },
  data() {
    return {
      title: '',
      description: '',
      narrative: '',
      expanded: false,
      qrels: [],
    }
  },
  methods: {
    fetchData() {
      if (this.show_topic) {
        get('/api/topic_description?ir_dataset_id=' + this.ir_dataset + '&topic_num=' + this.topic_num, this)
      }
    },
  },
  computed: {
    show_topic() {
      return this.ir_dataset + '' != 'null' &&  this.ir_dataset + '' != 'undefined' && this.topic_num + '' != 'null' &&  this.topic_num + '' != 'undefined';
    }
  },
  beforeMount() {
    this.fetchData();
  }
}
</script>
