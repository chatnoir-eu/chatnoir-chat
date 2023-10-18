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

<!--
    Hybrid index/search page view.
    Renders either the index or search view depending on whether a search query is given.
-->
<template>
<component :is="$route.query.q ? Search : Index" />
</template>

<script setup>
import Index from './Index'
import Search from './Search'
</script>
