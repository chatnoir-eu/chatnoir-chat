<!--
    Copyright 2021 Janek Bevendorff

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
-->
<template>
<div class="max-w-full h-full flex flex-row items-center mt-9 mb-5">
    <div class="block mx-auto max-w-full pb-52 sm:mb-64 text-center px-7">
        <cat-logo ref="catLogoElement" class="block h-40" />

        <search-field ref="searchFieldRef" v-model="searchModel" focus
                      @submit="search()" @change="$refs.catLogoElement.purr()" />
        <button type="button" class="chat-button"
                @click="goToChat">
           Chat with Chatnoir <inline-svg class="h-full mx-auto inline-block w-5" :src="require('@/assets/icons/chat.svg')" alt="Search" />
        </button>
    </div>
</div>
</template>

<script setup>
import { onMounted, ref } from "vue"
import { useRouter } from 'vue-router'

import CatLogo from '@/components/CatLogo'
import SearchField from '@/components/SearchField'
import { SearchModel } from '@/search-model'

const router = useRouter()
const searchFieldRef = ref(null)
const searchModel = ref(new SearchModel())

function search() {
    if (searchModel.value.query) {
        router.push({name: 'IndexSearch', query: searchModel.value.toQueryStringObj()})
    }
}

function goToChat() {
    router.push({name: 'Chat'})
}

onMounted(() => {
    searchModel.value.setIndices()
})
</script>

<style scoped>

.chat-button {
  /*background-color: #c34324;*/
  background: linear-gradient(45deg, #c34324, #da9c7d);;
  color: #0f0f0f;
  /*border: 1px solid #000000;*/
  border-radius: 20px;
  padding-inline: 8px;
  padding-block: 4px;
  display: block;
/*  position the element in the middle of its parent element*/
  margin-left: auto;
  margin-right: auto;
  margin-top: 20px;
  margin-bottom: 20px;
  height: 02em;

}

</style>
