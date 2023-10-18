<!--
    Search page view.

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
<header class="border-b mb-5 pt-5 -mx-5">
    <div class="mx-5">
        <div class="w-auto sm:hidden">
            <router-link to="/">
                <inline-svg class="inline-block h-10 max-w-full" :src="require('@/assets/img/chatnoir-icon.svg')" alt="" />
            </router-link>
        </div>
        <div class="flex flex-row items-center max-w-3xl mx-auto h-24">
            <div class="w-32 mr-6 hidden sm:block">
                <router-link to="/">
                    <cat-logo ref="catLogoElement" />
                </router-link>
            </div>

            <search-field ref="searchFieldRef" v-model="searchFieldModel" :focus="focus"
                          @submit="emitSubmit()" @change="$refs.catLogoElement.purr()" />
        </div>
    </div>

    <progress-bar :progress="requestProgress" class="mt-3" @complete="requestProgress = 0" />
</header>
</template>

<script setup>
import { onMounted, reactive, ref, toRef, watch } from 'vue'
import CatLogo from '@/components/CatLogo';
import SearchField from '@/components/SearchField';
import ProgressBar from '@/components/ProgressBar'
import { SearchModel } from '@/search-model'
import { useRoute } from 'vue-router'

const route = useRoute()
const emit = defineEmits(['update:modelValue', 'submit'])
const props = defineProps({
    action: {type: String, default:''},
    method: {type: String, default: "GET"},
    modelValue: {
        type: SearchModel,
        default: () => new SearchModel()
    },
    progress: {type: Number, default: 0},
    focus: {type: Boolean, default: false},
})

const searchFieldRef = ref(null)
const searchFieldModel = ref(null)
const requestProgress = ref(0)

async function emitSubmit() {
    emit('submit', searchFieldModel.value)
}

onMounted(() => {
    searchFieldModel.value = props.modelValue
    if (!searchFieldModel.value.query) {
        searchFieldModel.value.updateFromQueryString(route.query)
    }
})

watch(() => props.modelValue, (newValue) => {
    searchFieldModel.value = newValue
}, {deep: true})

watch(searchFieldModel, (newValue) => {
    emit('update:modelValue', newValue)
})

watch(toRef(props, 'progress'), (newValue) => {
    requestProgress.value = newValue
})

defineExpose({
    focus: (options = {}) => searchFieldRef.value.focus(options),
    blur: () => searchFieldRef.value.blur()
})
</script>
