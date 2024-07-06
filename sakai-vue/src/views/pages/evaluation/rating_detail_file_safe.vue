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
  {label: "安全性评分"}
]); //

const file_score = JSON.parse(window.localStorage.getItem('file_score'));
console.log('file_score', file_score);
console.log('file_score', file_score.security.score);

const rating = ref(10*file_score.security.score)
</script>

<template>
    <Breadcrumb :home="home" :model="items" />
    <br>
    <Card style="width: 70%">
        <template #title>安全性评分</template>
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
            <div class="text-900 font-medium text-xl">{{file_score.security.evaluations}}</div>
        </template>
    </Card>
    <br />
    <Card style="width: 70%">
        <template #title>改进建议</template>
        <template #content>
            <div class="text-900 font-medium text-xl">{{ file_score.security.suggestions }}</div>
        </template>
    </Card>
</template>
