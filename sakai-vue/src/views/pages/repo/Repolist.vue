<script setup>
import Card from 'primevue/card';
import { onMounted, ref } from 'vue';
import { ProductService } from '@/service/ProductService';
import Tag from 'primevue/tag';
import axios from 'axios';
const productService = new ProductService();
const repos_list = ref(null);
import ProgressSpinner from "primevue/progressspinner";

// 假设你的JWT令牌存储在localStorage中
const token = localStorage.getItem('token');
// 设置默认的Authorization头，自动附带认证头
axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
onMounted(() => {
    productService.getProducts().then((data) => {
        repos_list.value = data;
    });
});

const evaluate_request = (repo) => {
    console.log('评估请求');
    alert('正在评估，请稍后...');

    // 参数
    const repo_url = repo.Link;
    // 输出repo_url
    console.log('repo:', repo);

    // 发起GET请求到后端
    axios
        .get('/api/spark/generate_repo_json_secure', {
            params: {
                repo_url: repo_url
            }
        })
        .then((response) => {
            console.log('成功获取数据:', response.data);
            // 在这里处理返回的数据
        })
        .catch((error) => {
            console.error('获取数据失败:', error);
            // 处理错误
        });
};

const redirect_to_result = (repo) => {
    console.log('查看结果');
    // alert('跳转到结果界面');
    window.localStorage.setItem('repo_url', repo.Link); 
    window.localStorage.setItem('repo_name', repo.Name);
    // window.localStorage.setItem('repo_score', repo.score);
    window.location.href = '/pages/home';
};
</script>

<template>
    <div v-for="repo in repos_list">
        <Card style="width: 90%; overflow: hidden">
            <template #title>{{ repo.Name }} </template>

            <template #subtitle>{{ repo.Link }}</template>
            <template #content>
                <div style="display: flex; justify-content: space-between; align-items: flex-start">
                    <p class="m-0">
                        <!--                    {{ repo.reame }}-->
                        {{ repo.Description }}
                    </p>
                    <!--                此处根据数据库评估状态显示，暂时设置为点击评估，就会改变-->

                    <Tag v-if="repo.status === '未评估'" severity="warning" value="未评估" rounded></Tag>
                    <ProgressSpinner v-else-if="repo.status==='评估中'" style="width: 5vh; height: 5vh; margin:0;" :strokeWidth="4" />
                    <Tag v-else-if="repo.status === '已评估'" severity="success" value="已评估" rounded></Tag>
                </div>
            </template>
            <template #footer>
                <div class="flex gap-4 mt-1">
                    <Button label="评估" @click="evaluate_request(repo)" severity="secondary" />
                    <Button label="查看结果" @click="redirect_to_result(repo)" :disabled="repo.status !== '已评估'" />
                </div>
            </template>
        </Card>
        <br />
    </div>
</template>
