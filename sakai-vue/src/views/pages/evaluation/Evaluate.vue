<script>
import Filetree from './components/tree.vue';
import Tableview from './components/Tableview.vue';
import axios from 'axios';
const token = localStorage.getItem('token');
// 设置默认的Authorization头，自动附带认证头
axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

export default {
    name: 'evaluate',
    components: { Filetree, Tableview }
};
</script>
<script setup>
import { ref } from 'vue';
import { onMounted } from 'vue';

const fileinfo = ref(null);
const selectedNode = ref(null); //选中的node
// const props = defineProps(['repo_info']);
const repo_url = window.localStorage.getItem('repo_url');
const repo_name = window.localStorage.getItem('repo_name');
const fetchFileInfo = async () => {
    console.log('repo_info', repo_name);
    axios
        .get('/api/spark/view_repo_json_secure/', {
            params: {
                repo_url: repo_url
            }
        })
        .then((response) => {
            fileinfo.value = response.data.root;
        })
        .catch((error) => {
            console.error('Error fetching file info:', error);
        });
};
// fetchFileInfo();

onMounted(fetchFileInfo);

const handleNodeSelected = (node) => {
    console.log('handle param:', node);
    selectedNode.value = node;
    console.log('selectedNode', selectedNode.value);

    console.log('Node selected');
};
</script>

<template>
    <div class="evaluate-container">
        <div class="info-container">
            <p v-if="selectedNode">当前选中文件为：{{ selectedNode.key }}</p>
            <p v-else>请选择一个文件</p>
        </div>
        <div class="main-container">
            <div class="left-side">
                <Filetree :fileinfo="fileinfo" @node-selected="handleNodeSelected" />
            </div>
            <div class="right-side">
                <Tableview :select-node="selectedNode" />
            </div>
        </div>
    </div>
</template>

<style>
.evaluate-container {
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: #f0f0f0;
    padding: 20px; /* 添加一些内边距 */
}

.info-container {
    width: 100%;
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 10px 20px; /* 添加内边距 */
    margin-bottom: 10px; /* 添加下外边距 */
}

.main-container {
    display: flex;
    width: 100%;
    height: 100%;
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.left-side,
.right-side {
    height: 100%;
}

.left-side {
    width: 40%;
    background-color: #f9f9f9;
    border-right: 1px solid #ccc;
}

.right-side {
    width: 60%;
    background-color: #ffffff;
}
</style>
