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
<teleport to="body">
    <transition name="fade" @enter="enterHandler()">
        <div v-if="modalState"
             class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 border border-gray-700 flex items-center"
             @click.self="cancel()" @keyup.enter="confirm()" @keyup.esc="cancel()">
            <section ref="modalMain" tabindex="-1" class="bg-white rounded-md -mt-28 mx-auto shadow shadow-md overscroll-auto flex flex-col outline-none">
                <header class="h-4 flex flex-row border-b border-gray-200 rounded-t-lg bg-gray-100 mb-4 pt-4 pb-9 px-6">
                    <h2 class="flex-grow text-lg font-bold"><slot name="header" /></h2>
                    <button ref="closeButton" title="Close"
                            class="text-gray-700 -mr-1 h-6 w-6 ml-6 align-middle text-center border-2 border-transparent rounded-full
                            outline-none hover:text-red-600 focus:text-red-600 hover:border-red-600 focus:border-red-600"
                            @click.prevent="cancel()">
                        <inline-svg :src="require('@/assets/icons/close.svg')" class="h-full p-0.5 mx-auto" aria-label="Close" />
                    </button>
                </header>
                <div class="px-5 pb-4">
                    <slot />
                </div>
            </section>
        </div>
    </transition>
</teleport>
</template>

<script setup>
import { onMounted, onUnmounted, ref, toRef, watch } from 'vue';

const modalMain = ref(null)
const closeButton = ref(null)
const modalState = ref(false)

const props = defineProps({
    modelValue: {type: Boolean, default: false}
})
const emit = defineEmits(['update:modelValue', 'confirm', 'cancel'])

watch(toRef(props, 'modelValue'), (newValue, oldValue) => {
    if (newValue === oldValue) {
        return;
    }
    if (!newValue) {
        close()
    } else {
        modalState.value = newValue
    }
})

function enterHandler() {
    modalMain.value.focus()
}

function confirm() {
    emit('confirm')
    close()
}

function cancel() {
    emit('cancel')
    close()
}

function close() {
    modalState.value = false
    emit('update:modelValue', false)
}

onMounted(() => {
    modalState.value = props.modelValue
})

onUnmounted(() => {
    if (modalState.value) {
        close()
    }
})

defineExpose([
    cancel,
    close
])
</script>
