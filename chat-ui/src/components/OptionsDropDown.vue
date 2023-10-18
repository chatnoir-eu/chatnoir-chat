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
<ToolTipPopup class="tail-top">
    <fieldset>
        <legend class="font-bold mb-2">
            Select Indices:
        </legend>
        <ul class="pl-2">
            <li class="pb-0.5">
                <input id="select-all" class="chk ml-0" type="checkbox" :checked="allChecked()"
                       @click="toggleAllIndices($event.target.checked)">
                <label for="select-all">(Select All)</label>
            </li>
            <li v-for="(idx, pos) in modelValue" :key="idx.id" class="pb-0.5">
                <input :id="idx.id" name="index" class="chk ml-0 pb-1" type="checkbox"
                       :checked="idx.selected" :value="idx.id"
                       @click="toggleIndex(pos, $event.target.checked)">
                <label :for="idx.id">{{ idx.name }}</label>
            </li>
        </ul>
    </fieldset>
</ToolTipPopup>
</template>

<script setup>
import ToolTipPopup from '@/components/ToolTipPopup'

const emit = defineEmits(['update:modelValue'])
const props = defineProps({
    modelValue: {type: Array, default: () => []}
})

function allChecked() {
    for (let idx in props.modelValue) {
        if (!props.modelValue[idx].selected) {
            return false
        }
    }
    return true
}

function toggleAllIndices(on) {
    const mv = Array.from(props.modelValue)
    for (let idx in mv) {
        mv[idx].selected = on
    }
    emit('update:modelValue', mv)
}

function toggleIndex(pos, on) {
    const mv = Array.from(props.modelValue)
    mv[pos].selected = on
    emit('update:modelValue', mv)
}
</script>
