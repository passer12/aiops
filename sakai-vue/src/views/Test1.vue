<script>
import axios from 'axios';

export default {
    name: 'Test1',
    data() {
        return {
            message: 'Hello Vue!',
            now_time: null
        };
    },
    mounted() {
        axios
            .get('/api/gettime')
            .then((response) => {
                this.now_time = response.data.now_time;
            })
            .catch((error) => {
                console.log(error);
            });
    }
};
</script>

<template>
    <div>
        <h1>Test1</h1>
        <h2>{{ message }}</h2>
        <p>now_time is : {{ now_time }}</p>
    </div>
</template>

<style scoped></style>
