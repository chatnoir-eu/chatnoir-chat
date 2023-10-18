<template>
<div :class="$style.indicator"><div :class="colorCls"></div><div :class="colorCls"></div><div :class="colorCls"></div><div :class="colorCls"></div></div>
</template>

<script setup>
const props = defineProps({
    colorCls: {default: 'bg-red-300'}
})
</script>

<!-- Adjusted CSS-only loading indicator from https://loading.io/css/ -->
<style module>
.indicator {
    display: inline-block;
    position: relative;
    width: 4.5em;
    height: .8em;
}
.indicator div {
    position: absolute;
    top: 0;
    width: .8em;
    height: .8em;
    border-radius: 50%;
    animation-timing-function: cubic-bezier(0, 1, 1, 0);
}
.indicator div:nth-child(1) {
    left: 0.5em;
    animation: indicator1 0.6s infinite;
}
.indicator div:nth-child(2) {
    left: 0.5em;
    animation: indicator2 0.6s infinite;
}
.indicator div:nth-child(3) {
    left: 2em;
    animation: indicator2 0.6s infinite;
}
.indicator div:nth-child(4) {
    left: 3.5em;
    animation: indicator3 0.6s infinite;
}
@keyframes indicator1 {
    0% {
        transform: scale(0);
    }
    100% {
        transform: scale(1);
    }
}
@keyframes indicator3 {
    0% {
        transform: scale(1);
    }
    100% {
        transform: scale(0);
    }
}
@keyframes indicator2 {
    0% {
        transform: translate(0, 0);
    }
    100% {
        transform: translate(1.5em, 0);
    }
}
</style>
