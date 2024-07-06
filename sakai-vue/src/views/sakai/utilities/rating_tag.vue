<script setup>
import { ref } from 'vue';
import Tag from 'primevue/tag';

const props = defineProps(['rate'])
console.log(props.rate)
</script>

<template>
    <Tag v-if="rate > 8" icon="pi pi-check" severity="success" value="很好"></Tag>
    <Tag v-else-if="rate > 6" icon="pi pi-info-circle" severity="info" value="好"></Tag>
    <Tag v-else-if="rate > 4" icon="pi pi-exclamation-triangle" severity="warning" value="差"></Tag>
    <Tag v-else icon="pi pi-times" severity="danger" value="极差"></Tag>
</template>