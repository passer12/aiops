<script setup>
import store from '@/store';

store.commit('login');
</script>

<template>
    <router-view />
</template>

<style scoped></style>
