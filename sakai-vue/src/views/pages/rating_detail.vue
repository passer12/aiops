<script setup>
import ProgressBar from 'primevue/progressbar';
import { ref } from 'vue';

// breadcrumb区域
const home = ref({
    icon: 'pi pi-home',
    to: '/pages/profile'
});
const reponame = ref(window.localStorage.getItem('repo_name') ? window.localStorage.getItem('repo_name') : 'examplerepo');
const items = ref([{ label: window.localStorage.getItem('username'), url: '/pages/profile' },
  { label: reponame },
  {label: "可读性评分"}
]); //

</script>

<template>
    <Breadcrumb :home="home" :model="items" />
    <br>
    <Card style="width: 70%">
        <template #title>可读性评分</template>
        <template #content>
            <div class="text-900 font-medium text-xl">{{ 0.5 }}</div>
            <br />
            <ProgressBar :value="50" style="width: 50%"></ProgressBar>
        </template>
    </Card>
    <br />

    <Card style="width: 70%">
        <template #title>代码评价</template>
        <template #content>
            <div class="text-900 font-medium text-xl">不写注释</div>
        </template>
    </Card>
    <br />
    <Card style="width: 70%">
        <template #title>改进建议</template>
        <template #content>
            <div class="text-900 font-medium text-xl">重写吧</div>
        </template>
    </Card>
</template>
