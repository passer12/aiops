<script setup>
import ProgressBar from 'primevue/progressbar';
import { ref } from 'vue';
import Knob from 'primevue/knob';
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

const rating = ref(50)
</script>

<template>
    <Breadcrumb :home="home" :model="items" />
    <br>
    <Card style="width: 70%">
        <template #title>可读性评分</template>
        <template #content>
<!--            <div class="text-900 font-medium text-xl">{{ rating }}</div>-->
            <div style="width:40%" class="card flex justify-center">
                <Knob v-model="rating" :size="100" />
            </div>
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
