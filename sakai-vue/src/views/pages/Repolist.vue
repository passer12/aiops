<script setup>
import Card from 'primevue/card';
import {onMounted, ref} from 'vue';
import { ProductService } from '@/service/ProductService';
import  Tag from 'primevue/tag';
import axios from 'axios';
const productService = new ProductService();
const repos_list = ref(null);

// 假设你的JWT令牌存储在localStorage中
const token = localStorage.getItem('token');
// 设置默认的Authorization头，自动附带认证头
axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

onMounted(() => {
    productService.getProducts().then(data => {
        repos_list.value = data;
    });
});

const evaluate_request = (repo) => {
    console.log('评估请求');
    alert("评估一波,导到一个等待界面");

    // 参数
    const repo_url = repo.Link;
    // 输出repo_url
    console.log('repo:', repo);

    // 发起GET请求到后端
    axios.get('/api/spark/generate_repo_json_secure', {
        params: {
            repo_url: repo_url
        }
    })
    .then(response => {
        console.log('成功获取数据:', response.data);
        // 在这里处理返回的数据
    })
    .catch(error => {
        console.error('获取数据失败:', error);
        // 处理错误
    });
};


const redirect_to_result = (reponame) => {
  console.log('查看结果');
  alert("跳转到结果界面")
  window.localStorage.setItem("repo_name", reponame) //后端不完备，暂时出此下策
  window.location.href = "/dashboard"
}
</script>

<template>
    <div v-for="repo in repos_list">

        <Card style="width: 90%; overflow: hidden">
            <template #title>{{ repo.Name }}
            </template>

            <template #subtitle>{{ repo.Description }}</template>
            <template #content>
              <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <p class="m-0">
<!--                    {{ repo.reame }}-->
                  这里应该有一个字段,也许是readme之类的
                </p>
<!--                此处根据数据库评估状态显示，暂时设置为点击评估，就会改变-->

                 <Tag v-if="repo.Link == 0" icon="pi pi-check" severity="success" value="已评估"></Tag>
                  <Tag v-else severity="warning" value="未评估" rounded></Tag>
                </div>
            </template>
            <template #footer>
                <div class="flex gap-4 mt-1">
                    <Button label="评估" @click="evaluate_request(repo)" severity="secondary" />
                    <Button label="查看结果" @click="redirect_to_result(repo.Name)" />
                </div>
            </template>
        </Card>
      <br> </br>
    </div>
</template>
