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
<!-- eslint-disable vue/no-v-html -->
<article :id="'result-' + data.uuid" class="my-8">
    <header class="leading-tight break-words">
        <a v-if="data.targetUri" :href="data.targetUri" rel="nofollow"
           class="text-gray-800 visited:text-gray-800 text-sm">
            {{ abbreviateUrl(data.targetUri, 2).replace(/^https?:\/\//i, '') }}
        </a>
        <h2 :class="$style.title" class="leading-none">
            <a :href="data.cacheUri" rel="nofollow" class="text-xl text-red-700" v-html="data.title"></a>
        </h2>
        <div class="text-sm text-gray-800 mt-0.5">
            <span v-if="data.authors && data.authors.length > 0" :class="$style['meta-link']">
                <a :href="getAuthorUrl(data.authors[0])">{{ getLastName(data.authors[0]) }}</a>
                <span v-if="data.authors.length === 2"> and </span>
                <a v-if="data.authors.length === 2" :href="getAuthorUrl(data.authors[1])">{{ getLastName(data.authors[1]) }}</a>
                <span v-if="data.authors.length > 2"> et al.</span>
            </span>

            <span v-if="data.index && data.warcId" :class="$style['meta-link']">
                <a :href="getQueryUrl(route, `index:${data.index} ${meta.queryString.replace(RegExp(`index:${data.index}\\s+`), '')}`, null)">
                    {{ getFullIndexName() }}
                </a>
            </span>

            <span v-if="data.venue" :class="$style['meta-link']">
                <a :href="getQueryUrl(route, `venue:${data.venue}`)">{{ data.venue }}</a>
            </span>

            <span v-if="data.year" :class="$style['meta-link']">
                <a :href="getQueryUrl(route, `year:${data.year}`)">{{ data.year }}</a>
            </span>

            <span v-if="!data.year && data.crawlDate" :class="$style['meta-link']">
                Crawled {{ new Intl.DateTimeFormat('en-US', {month: 'short', year: 'numeric'}).format(Date.parse(data.crawlDate)) }}
            </span>

            <button ref="detailsButton" type="button" class="w-3 h-3 ml-3 -mt-0.5 text-center align-middle inline-block" @click="detailsShown = !detailsShown">
                <inline-svg :src="require('@/assets/icons/settings.svg')" class="h-full mx-auto align-middle" aria-label="Details" />
            </button>

            <ToolTipPopup :visible="detailsShown" :aria-hidden="(!detailsShown).toString()" :ref-element="$refs.detailsButton"
                          class="tail-top max-w-lg" @close="detailsShown = false">
                <dl :class="$style['meta-details']">
                    <dt>Score:</dt>
                    <dd>{{ data.score.toFixed(2) }}</dd>

                    <dt>Index:</dt>
                    <dd>{{ getFullIndexName() }}</dd>

                    <dt>Document ID:</dt>
                    <dd class="font-mono text-2xs"><CopyableStringField>{{ data.uuid }}</CopyableStringField></dd>

                    <dt v-if="data.warcId">WARC ID:</dt>
                    <dd v-if="data.warcId" class="font-mono text-2xs"><CopyableStringField>{{ data.warcId }}</CopyableStringField></dd>

                    <dt v-if="data.trecId">TREC ID:</dt>
                    <dd v-if="data.trecId" class="font-mono text-2xs"><CopyableStringField>{{ data.trecId }}</CopyableStringField></dd>

                    <dt v-if="data.pageRank">Page Rank:</dt>
                    <dd v-if="data.pageRank">{{ data.pageRank }}</dd>

                    <dt v-if="data.spamRank">Spam Rank:</dt>
                    <dd v-if="data.spamRank">{{ data.spamRank }}</dd>

                    <dt v-if="data.doi">DOI:</dt>
                    <dd v-if="data.doi"><a :href="data.targetUri" rel="nofollow">{{ data.doi }}</a></dd>

                    <dt v-if="data.anthologyId">Anthology ID:</dt>
                    <dd v-if="data.anthologyId">{{ data.anthologyId }}</dd>

                    <dt v-if="data.authors">Authors:</dt>
                    <dd v-if="data.authors">
                        <span v-for="(a, i) in data.authors.slice(0, authorsShowMore || data.authors.length === maxAuthors + 1 ?
                            data.authors.length : maxAuthors)" :key="a">
                            <a :href="getAuthorUrl(a)">{{ a.replace(/\s+/, '\u00a0') }}</a>
                            <span v-if="i !== data.authors.length - 1">,<br></span>
                        </span>

                        <a v-if="data.authors.length > maxAuthors + 1" href="#" class="block clear-left"
                           @click.prevent="authorsShowMore = !authorsShowMore">
                            {{ authorsShowMore ? 'Show less\u2026' : `+${data.authors.length - maxAuthors} more\u2026` }}
                        </a>
                    </dd>

                    <dt v-if="data.venue">Venue:</dt>
                    <dd v-if="data.venue">{{ data.venue }}</dd>

                    <dt v-if="data.year">Year:</dt>
                    <dd v-if="data.year">{{ data.year }}</dd>

                    <dt v-if="data.lang">Language:</dt>
                    <dd v-if="data.lang">{{ data.lang }}</dd>

                    <dt v-if="data.contentType">Content-Type:</dt>
                    <dd v-if="data.contentType">{{ data.contentType }}</dd>

                    <dt v-if="data.crawlDate">Crawl Date:</dt>
                    <dd v-if="data.crawlDate">
                        {{ new Intl.DateTimeFormat('en-US', {dateStyle: 'medium', timeStyle: 'long'}).format(Date.parse(data.crawlDate)) }}
                    </dd>
                </dl>

                <div class="clear-left ml-28 mt-2">
                    <a href="#" @click.prevent="explainModalState = true">Explain Ranking&hellip;</a>
                    <modal-dialog v-if="explainModalState" v-model="explainModalState">
                        <template #header>
                            Explain Ranking
                        </template>
                        Sorry, but this feature is not yet implemented.
                    </modal-dialog>
                </div>
            </ToolTipPopup>
        </div>
    </header>

    <p :class="$style.snippet" class="text-gray-900 mt-1" v-html="data.snippet"></p>
</article>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';

import { abbreviateUrl, getQueryUrl } from '@/common'

import ToolTipPopup from '@/components/ToolTipPopup'
import ModalDialog from '@/components/ModalDialog'
import CopyableStringField from '@/components/CopyableStringField'

const maxAuthors = 6
const detailsShown = ref(false)
const authorsShowMore = ref(false)
const explainModalState = ref(false)

const props = defineProps({
    data: {type: Object, default: () => {}},
    meta: {type: Object, default: () => {}}
})
const route = useRoute()

function getAuthorUrl(author) {
    return getQueryUrl(route, `author:"${author}"`)
}

function getLastName(author) {
    return author.split(/\s+/).pop()
}

function getFullIndexName() {
    return props.meta.indices.find((e) => e.id === props.data.index).name
}
</script>

<style module>
.title em, .snippet em {
    @apply font-bold;
    @apply not-italic;
}

.meta-link:not(:first-child)::before {
    content: '·';
    display: inline-block;
    @apply mx-1.5;
}

.meta-link a {
    @apply text-gray-800;
}

.meta-details {
    dt {
        @apply font-bold text-right;
        @apply float-left w-24 clear-left;
    }

    dd {
        @apply ml-28;
    }
}
</style>
