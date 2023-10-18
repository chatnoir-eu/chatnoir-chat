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
<span class="group inline-block nowrap relative pr-3.5">
    <span ref="focusElement" class="group outline-none inline-block focus:ring-1 focus:ring-offset-0 focus:ring-red-300" tabindex="0"
          @click="select()" @keyup.enter="select(true)" @keyup.space="select(true)">
        <slot />
        <button class="absolute group-hover:inline-block group-focus:inline-block h-3
                       text-gray-600 hover:text-red-400 focus:text-red-400 active:text-red-700 right-0 -top-0.5 hidden"
                aria-label="Copy" tabindex="-1" @click="copy()">
            <inline-svg :src="require('@/assets/icons/copy.svg')" class="h-full" />
        </button>
    </span>
</span>
</template>

<script setup>
import { ref } from 'vue';

const focusElement = ref(null)

function select(force = false) {
    focusElement.value.focus()

    const sel = window.getSelection()

    // Only do automatic selection if user clicked without dragging
    if (force || sel.anchorOffset === sel.focusOffset) {
        const range = document.createRange()
        range.setStartBefore(focusElement.value)
        range.setEndAfter(focusElement.value)

        sel.removeAllRanges()
        sel.addRange(range)
    }
}

function copy() {
    select(window.getSelection() && !focusElement.value.contains(window.getSelection().focusNode))
    document.execCommand('copy')
}
</script>
