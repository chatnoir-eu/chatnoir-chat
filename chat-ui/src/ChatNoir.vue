<template>
<section id="app" class="flex flex-col">
    <main class="flex-grow w-full">
        <router-view :key="$route.path" />
    </main>

<!--    <webis-footer-->
<!--        copyright-start-year="2012"-->
<!--        :additional-links="[-->
<!--            {href: 'https://webis.de/publications.html', anchor: 'Cite'}]"-->
<!--    />-->
</section>
</template>

<script setup>
import { onMounted } from 'vue'
import WebisFooter from '@/components/WebisFooter'

onMounted(() => {
    // Hide browser address bar
    setTimeout(() => window.scrollTo(0, 1), 0)
})
</script>
