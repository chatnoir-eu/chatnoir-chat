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
<div class="max-w-full px-5">
    <search-header v-model="searchHeaderModel" :progress="requestProgress" @submit="redirectSearch()" />

    <div class="max-w-3xl mx-auto mt-10">
        <div v-if="$route.name === 'ApikeyRequest'">
            <h1 class="text-2xl font-bold my-3">Request a ChatNoir API key</h1>

            <p class="my-3">Purr&hellip; Thank you for your interest in ChatNoir, we are glad to see you here!</p>
            <p class="my-3">
                We offer free API keys for members of verified research institutes. If you qualify for a free API key, you can
                apply by clicking the button below. We will review your request and you will receive your API key by email once approved.
            </p>
            <p class="my-3">
                Alternatively, if you have a ChatNoir passcode, you can use it to issue a (usually time-limited)
                API key immediately.
            </p>

            <div class="my-10 text-center">
                <button class="btn input-xl primary mx-4" @click="$router.push({name: 'ApikeyRequest_Academic'})">Apply for a free API key</button>
                <button class="btn input-xl mx-4" @click="$router.push({name: 'ApikeyRequest_Passcode'})">I have a passcode</button>
            </div>
        </div>

        <div v-else-if="$route.name === 'ApikeyRequest_Academic' || $route.name === 'ApikeyRequest_Passcode'">
            <h1 class="text-2xl font-bold my-3">Request a ChatNoir API key</h1>

            <div v-if="isAcademic()">
                <p class="my-3">
                    We offer free API keys for members of verified research institutes for academic use.
                </p>
                <p class="my-3">
                    To apply for a free academic API key, please enter your personal details and affiliation below.
                    We will verify your request and you will receive your API key within 1&ndash;2 working days if eligible.
                </p>
                <p class="my-3">
                    If you do not qualify for a free API key or need a key for non-academic purposes, please contact us directly,
                    so we can assess your use case and potentially work out an agreement.
                </p>
            </div>
            <div v-else>
                <p class="my-3">
                    If you have a ChatNoir passcode, you can use it to issue an API key to yourself. Passcodes are handed out at special
                    events such as shared tasks, so participants can obtain their own personal API keys. API keys issued via
                    passcodes are bound to a specific event and are usually time-limited.
                </p>
                <p class="my-3">
                    If you are a shared task organizer yourself and want a passcode for your participants, please contact us by email with details
                    about your task and we will be more than happy to help you out.
                </p>
            </div>

            <h2 v-if="isAcademic()" class="text-lg font-bold mt-8 mb-4">API key request form (academic):</h2>
            <h2 v-else class="text-lg font-bold mt-8 mb-4">API key request form (passcode):</h2>

            <form ref="requestFormRef" action="" method="post" novalidate class="sm:ml-1 mb-20" @submit.prevent="submitForm()">
                <form-field ref="formNameField" v-model="form.commonName" name="common_name"
                            placeholder="Name which key will be issued to" :validator="v$.commonName">
                    Name
                </form-field>
                <form-field v-model="form.email" name="email" type="email" :validator="v$.email"
                            :placeholder="isAcademic() ? 'Email address issued by your institute' : 'Email address for sending the key'">
                    Email address
                </form-field>

                <form-field v-if="isAcademic()" v-model="form.organization" name="organization" placeholder="Academic institute (full name)"
                            :validator="v$.organization" class="my-3 mb-10">
                    Organization
                </form-field>
                <form-field v-else v-model="form.organization" name="organization" class="my-3 mt-10">Organization</form-field>

                <form-field v-model="form.address" :validator="v$.address" name="address">Postal address</form-field>
                <form-field v-model="form.zip_code" :validator="v$.zip_code" name="zip_code">ZIP code</form-field>
                <form-field v-model="form.state" :validator="v$.state" name="state">Federal State</form-field>
                <form-field-country v-model="form.country" :validator="v$.country" name="country" type="select">Country</form-field-country>

                <form-field v-if="isAcademic()" v-model="form.comments" name="comments" type="textarea" class="my-3 mt-10"
                            placeholder="Please give a short description (max. 200 characters)" :validator="v$.comments">
                    What will you use the API key for?
                </form-field>

                <form-field v-if="!isAcademic()" v-model="form.passcode" name="passcode" class="my-3 mt-10" :validator="v$.passcode">Passcode</form-field>

                <form-field v-model="form.tosAccepted" name="tos_accepted" type="checkbox" class="mt-10" :validator="v$.tosAccepted">
                    I confirm that I will use the API key for <strong>academic purposes only</strong> and agree to the
                    <a href="https://webis.de/legal.html" target="_blank"><strong>Webis Terms of Service</strong></a>.
                </form-field>
                <form-field v-model="form.privacyAccepted" name="privacy_accepted" type="checkbox" :validator="v$.privacyAccepted">
                    I agree to the <a href="https://webis.de/legal.html#privacy" target="_blank"><strong>Webis Privacy Policy</strong></a>.
                </form-field>

                <div class="my-10">
                    <input v-if="isAcademic()"
                           type="submit" value="Request Academic API Key" class="btn input-lg primary mr-4">
                    <input v-else type="submit" value="Request API Key" class="btn input-lg primary mr-4">
                    <button class="btn input-lg" @click.prevent="cancelModalState = true">Cancel and Go Back</button>
                    <loading-indicator v-if="requestProgress > 0" class="ml-3" />
                </div>
            </form>
        </div>

        <div v-else-if="$route.name === 'ApikeyRequest_Received'">
            <h1 class="text-2xl font-bold my-3">Thank you!</h1>
            <p class="my-3">
                {{ $route.meta.message }}
            </p>
        </div>

        <div v-else-if="$route.name === 'ApikeyRequest_Verified'">
            <div v-if="$route.query.success !== undefined">
                <h1 class="text-2xl font-bold my-3">Email verified</h1>
                <p class="my-3">Thanks! Your email has been verified.</p>
                <p v-if="$route.query.passcode !== undefined">
                    Your new API key has been sent to you by email. If you do not receive a message within the next few
                    minutes, please check your spam folder.
                </p>
                <p v-else>
                    We have received your API key request and will review it within the next few days.
                </p>
            </div>
            <div v-else-if="$route.query.already_verified !== undefined">
                <h1 class="text-2xl font-bold my-3">No need :-)</h1>
                <p class="my-3">Your email address has been verified already.</p>
            </div>
            <div v-else>
                <h1 class="text-2xl font-bold my-3">Error!</h1>
                <p class="my-3">
                    Your email address could not be verified<span v-if="$route.query.error"> ({{ $route.query.error }})</span>.
                </p>
            </div>
        </div>
    </div>

    <modal-dialog v-if="cancelModalState" v-model="cancelModalState" @confirm.enter="cancelModal()" @cancel="cancelModal()">
        <template #header>
            Cancel API key application?
        </template>
        <div class="m-3">
            <p>Do you want to discard all input and cancel the application process?</p>
            <div class="text-center mt-6">
                <button class="btn input-lg mx-2" @click.prevent="cancelApplication()">Cancel Application</button>
                <button class="btn primary input-lg mx-2" @click.prevent="cancelModal()">Go Back To Form</button>
            </div>
        </div>
    </modal-dialog>
</div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import useVuelidate from '@vuelidate/core'
import axios from 'axios'
import { email, helpers, required, requiredIf, sameAs } from '@vuelidate/validators'

import SearchHeader from '@/components/SearchHeader'
import ModalDialog from '@/components/ModalDialog'
import { SearchModel } from '@/search-model'
import FormField from '@/components/FormField'
import FormFieldCountry from '@/components/FormFieldCountry'
import LoadingIndicator from '@/components/LoadingIndicator'
import { getCsrfToken } from '@/common'

const router = useRouter()
const route = useRoute()
const searchHeaderModel = ref(new SearchModel())

const cancelModalState = ref(false)
const requestProgress = ref(0)

let routeGuardDestination = null

const requestFormRef = ref(null)
const form = reactive({
    commonName: '',
    email: '',
    organization: '',
    address: '',
    zip_code: '',
    state: '',
    country: '',
    comments: '',
    passcode: '',
    tosAccepted: false,
    privacyAccepted: false,
})
const $externalResults = ref({})

const rules = computed(() => {
    const tosMsg = helpers.withMessage('You must accept the Terms of Service', sameAs(true))
    const privacyMsg = helpers.withMessage('You must accept the Privacy Policy', sameAs(true))
    return {
        commonName: {required},
        email: {required, email},
        address: {_: () => true},   // stub validator, otherwise `null` will be passed to <form-field />
        zip_code: {_: () => true},
        state: {_: () => true},
        country: {_: () => true},
        organization: {required: requiredIf(isAcademic)},
        comments: {required: requiredIf(isAcademic)},
        tosAccepted: {required: tosMsg},
        privacyAccepted: {required: privacyMsg},
        passcode: {required: requiredIf(() => !isAcademic())},
    }
})
const v$ = useVuelidate(rules, form, {$externalResults})
const formNameField = ref(null)


function isAcademic() {
    return route.name === 'ApikeyRequest_Academic'
}

function redirectSearch() {
    router.push({name: 'IndexSearch', query: searchHeaderModel.value.toQueryStringObj()})
}

function cancelApplication() {
    cancelModalState.value = false
    if (routeGuardDestination === null) {
        routeGuardDestination = {name: 'ApikeyRequest'}
    }
    router.push(routeGuardDestination)
}

function cancelModal() {
    routeGuardDestination = null
    cancelModalState.value = false
}

onMounted(() => {
    if (formNameField.value) {
        formNameField.value.focus()
    }
    routeGuardDestination = null

    if (route.name === 'ApikeyRequest_Received' && !route.meta.message) {
        router.push({name: 'ApikeyRequest'})
    }
})

router.beforeEach((to, from) => {
    if (to.name === 'ApikeyRequest_Received') {
        return true
    }

    // Request form route, guard with modal
    if (from.name === 'ApikeyRequest_Academic' || from.name === 'ApikeyRequest_Passcode') {
        if (routeGuardDestination === null) {
            routeGuardDestination = to
            cancelModalState.value = true
            return false
        }
    }

    // Not a request form route or modal has been shown and confirmed by the user
    routeGuardDestination = to
    return true
})

let serverMessage = null
router.beforeEach(async to => {
    if (to.name === 'ApikeyRequest_Received' && serverMessage) {
        to.meta.message = serverMessage
    }
})

async function submitForm() {
    $externalResults.value = {}
    if (!await v$.value.$validate()) {
        return
    }

    const requestOptions = {
        method: 'POST',
        url: route.path,
        headers: {
            'Content-Type': 'multipart/form-data',
            'X-CSRFToken': getCsrfToken()
        },
        data: new FormData(requestFormRef.value),
        onDownloadProgress(e) {
            requestProgress.value = Math.max(Math.round((e.loaded * 100) / e.total), requestProgress.value)
        }
    }

    const response = await axios(requestOptions)

    if (!response.data.valid) {
        Object.keys(response.data.errors).forEach((k) => {
            $externalResults.value[k] = response.data.errors[k].map((e) => e.message.replace(/\.$/, ''))
        })
    } else {
        serverMessage = response.data.message
        await router.push({name: 'ApikeyRequest_Received'})
    }
    setTimeout(() => requestProgress.value = 0, 150)
}
</script>
