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
<span aria-hidden="true" role="img">
    <inline-svg class="inline-block h-full w-auto max-w-full" :src="require('@/assets/img/chatnoir.svg')" alt=""
                @loaded="logoElement = $event" />
</span>
</template>

<script setup>
import { ref, watch } from 'vue';

const purrTimeout = ref(null)
const logoElement = ref(null)

function purr() {
    if (!logoElement.value) {
        return
    }
    if (purrTimeout.value !== null) {
        clearTimeout(purrTimeout.value)
    }

    const eyes = logoElement.value.querySelector('#Eyes')
    eyes.setAttribute('visibility', 'hidden')

    purrTimeout.value = setTimeout(() => {
        eyes.setAttribute('visibility', 'visible')
        purrTimeout.value = null
    }, 300)
}

watch(logoElement, () => {
    logoElement.value.querySelector('#Body').addEventListener('mousemove', purr)
})

defineExpose({
    purr
})
</script>
