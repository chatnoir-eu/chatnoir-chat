<!--
    Copyright 2022 Janek Bevendorff

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
<div v-if="isTextField()" :class="$props.class">
    <label v-if="$slots.default" :for="'form-' + $props.name" class="lbl-block" :class="labelCls()">
        <slot />
        <span v-if="!isValid()"> ({{ errors() }})</span>
        <span v-if="isRequired()"> *</span><span v-else> (optional)</span>
    </label>
    <select v-if="$props.type === 'select'"
            :id="'form-' + $props.name"
            ref="formFieldRef"
            v-model="model"
            :name="$props.name"
            :required="isRequired()"
            class="select md:w-1/2 w-full" :class="inputCls()"
            v-bind="$attrs"
            @blur="touch()">
        <option v-for="[value, text] of $props.options" :key="value" :value="value">{{ text }}</option>
    </select>
    <textarea v-else-if="$props.type === 'textarea'"
              :id="'form-' + $props.name"
              ref="formFieldRef"
              v-model="model"
              :name="$props.name"
              :required="isRequired()"
              :placeholder="$props.placeholder"
              class="text-field md:w-1/2 w-full" :class="inputCls()"
              v-bind="$attrs"
              @blur="touch()"></textarea>
    <input v-else
           :id="'form-' + $props.name"
           ref="formFieldRef"
           v-model="model"
           :type="$props.type"
           :name="$props.name"
           :required="isRequired()"
           :placeholder="$props.placeholder"
           class="text-field md:w-1/2 w-full" :class="inputCls()"
           v-bind="$attrs"
           @blur="touch()">
</div>
<div v-else :class="$props.class">
    <div v-if="!isValid()" class="form-error text-sm">{{ errors() }}</div>
    <input v-if="$props.type !== 'textarea'"
           :id="'form-' + $props.name"
           ref="formFieldRef"
           v-model="model"
           :type="$props.type"
           :name="$props.name"
           :required="isRequired()"
           :class="inputCls()"
           v-bind="$attrs">
    <label v-if="$slots.default" :for="'form-' + $props.name">
        <slot />
        <span v-if="isRequired()"> *</span>
    </label>
</div>
</template>

<script>
export default {
    inheritAttrs: false
}
</script>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
    modelValue: {},
    options: {},
    type: {type: String, default: 'text'},
    name: {type: String, required: true},
    placeholder: {type: String},
    class: {type: String, default: 'my-3'},
    validator: {type: Object, default: null},
})

const emit = defineEmits(['update:modelValue'])
const model = computed({
    get: () => props.modelValue,
    set: (value) => {
        emit('update:modelValue', value)
    }
})

const formFieldRef = ref(null)

function isTextField() {
    return props.type !== 'checkbox' && props.type !== 'radio'
}

function isValid() {
    if (!props.validator || !props.validator.$errors) {
        return true
    }
    return props.validator.$errors.length === 0
}

function isRequired() {
    if (!props.validator) {
        return false
    }
    for (let r of Object.keys(props.validator)) {
        if (r.startsWith('required')) {
            const p = props.validator[r]
            return (p.$params && typeof p.$params.prop === 'function') ? p.$params.prop() : true
        }
    }
    return false
}

function errors() {
    if (!props.validator) {
        return ''
    }
    return props.validator.$errors.map((e) => e.$message).join(', ')
}

function labelCls() {
    const cls = []
    if (isRequired()) {
        cls.push('lbl-required')
    }
    if (props.validator && !isValid(props.validator)) {
        cls.push('form-error')
    }
    return cls.join(' ')
}

function inputCls() {
    if (props.type === 'checkbox') {
        return 'chk'
    }
    if (props.type === 'radio') {
        return 'radio'
    }
    if (props.validator && !isValid(props.validator)) {
        return 'invalid'
    }
    return ''
}

function touch() {
    if (props.validator) {
        props.validator.$touch()
    }
}

defineExpose({
    blur: () => {
        formFieldRef.value.blur()
    },
    click: () => {
        formFieldRef.value.click()
    },
    focus: () => {
        formFieldRef.value.focus()
    },
    select: () => {
        formFieldRef.value.select()
    }
})
</script>
