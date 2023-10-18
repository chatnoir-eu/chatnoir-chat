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
<div ref="mainElement" class="h-0.5 w-full m-0 p-0 invisible overflow-hidden" aria-hidden="true">
    <div :class="$style['progress-bar']"
         class="h-full m-0 p-0 bg-red-400 rounded-r-full transition-width duration-150"
         :style="`width: ${displayedProgress}%`"></div>
</div>
</template>

<script setup>
import { onMounted, ref, toRef, watch } from 'vue'

const emit = defineEmits(['complete'])
const props = defineProps({
    progress: {type: Number, default: 0},
    fakeProgress: {type: Boolean, default: true}
})
const mainElement = ref(null)
const displayedProgress = ref(0)
let updateInterval = null

function updateProgress() {
    if (!mainElement.value || props.progress <= 0) {
        clearInterval(updateInterval)
        updateInterval = null
        return
    }

    mainElement.value.classList.remove('invisible')
    displayedProgress.value = Math.min(100, Math.max(displayedProgress.value, props.progress))
    if (props.fakeProgress && !updateInterval) {
        updateInterval = setInterval(() => {
            if (displayedProgress.value >= 95) {
                clearInterval(updateInterval)
                updateInterval = null
                return
            }
            displayedProgress.value = Math.min(
                95, displayedProgress.value + (1.0 / (1.0 + Math.exp(displayedProgress.value  / 10.0 - 3.0))))
        }, 50)
    }

    if (props.progress >= 100) {
        clearInterval(updateInterval)
        updateInterval = null
        setTimeout(() => {
            if (mainElement.value) {
                mainElement.value.classList.add('invisible')
            }
            displayedProgress.value = 0
            emit('complete')
        }, 200)
    }
}

watch(toRef(props, 'progress'), () => {
    updateProgress()
})

onMounted(() => {
    updateProgress()
})
</script>

<style module>
.progress-bar {
    transition: width 100ms;
}
</style>
