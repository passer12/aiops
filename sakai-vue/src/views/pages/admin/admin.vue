<script>
export default {
    data() {
        return {
            adminUrl: 'http://127.0.0.1:8000/admin'
        };
    }
};
</script>

<template>
    <div>
        <iframe :src="adminUrl" width="100%" height="1000px" frameborder="0"></iframe>
    </div>
</template>

<style scoped>
iframe {
    border: none;
}
</style>
