<script setup>
import { onMounted, ref } from 'vue';
import Tag from 'primevue/tag';
import Card from 'primevue/card';
import axios from 'axios';

import Paginator from 'primevue/paginator';

const token = localStorage.getItem('token');
// 设置默认的Authorization头，自动附带认证头
axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
const todays_history = ref(null);
const before_history = ref(null);
const username = localStorage.getItem('username');
const get_history = () => {
    axios
        .get('/api/repos/history/')
        .then((response) => {
            console.log(response.data);
            todays_history.value = response.data.today;
            before_history.value = response.data.before;
            console.log(todays_history.value);
        })
        .catch((error) => {
            console.error(error);
        });
};
onMounted(get_history);

</script>

<template>
    <div class="card">
        <div class="flex align-items-center justify-content-between mb-4">
            <h5>操作记录</h5>
        </div>
        <div class="history-container">
            <div class="left-part">
                <span class="block text-600 font-medium mb-3">TODAY</span>
                <ul class="p-0 mx-0 mt-0 mb-4 list-none">
                    <li v-for="history in todays_history" :key="history.id" class="flex align-items-center py-2 border-bottom-1 surface-border">
                        <div class="w-3rem h-3rem flex align-items-center justify-content-center bg-orange-100 border-circle mr-3 flex-shrink-0">
                            <i class="pi pi-history text-xl text-orange-500"></i>
                        </div>
                        <span class="text-700 line-height-3"
                            ><p>
                                <Tag v-if="history.status_code > 300" severity="warning" value="失败"></Tag>
                                <Tag v-else severity="success" value="成功"></Tag>
                                {{ username }}
                                <strong v-if="history.method === 'DELETE'">删除了</strong>
                                <strong v-else-if="history.method === 'POST'">新建了</strong>
                                <strong v-if="history.method === 'PATCH'">更新了</strong>
                                仓库 {{ history.payload }}
                            </p></span
                        >
                    </li>
                </ul>
            </div>

            <div class="right-part">
                <span class="block text-600 font-medium mb-3">Before</span>
                <ul class="p-0 mx-0 mt-0 mb-4 list-none">
                    <li v-for="history in before_history" :key="history.id" class="flex align-items-center py-2 border-bottom-1 surface-border">
                        <div class="w-3rem h-3rem flex align-items-center justify-content-center bg-orange-100 border-circle mr-3 flex-shrink-0">
                            <i class="pi pi-history text-xl text-orange-500"></i>
                        </div>
                        <span class="text-700 line-height-3"
                            ><p>
                                <Tag v-if="history.status_code > 300" severity="warning" value="失败"></Tag>
                                <Tag v-else severity="success" value="成功"></Tag>
                                {{ username }}
                                <strong v-if="history.method === 'DELETE'">删除了</strong>
                                <strong v-else-if="history.method === 'POST'">新建了</strong>
                                <strong v-if="history.method === 'PATCH'">更新了</strong>
                                仓库 {{ history.payload }}
                            </p></span
                        >
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<style scoped>
.history-container {
    display: flex;
    flex-direction: row;
    height: 100%;
}
.left-part {
    width: 50%;
    height: 100%;
}
</style>
