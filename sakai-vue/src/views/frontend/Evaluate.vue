<script>
import Filetree from './components/tree.vue';
import Tableview from './components/Tableview.vue';

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

const fetchFileInfo = async () => {
    try {
        const response = await fetch('/demo/data/treenodes.json');
        const data = await response.json();
        console.log('data', data);
        fileinfo.value = data.root;
    } catch (error) {
        console.error('Error fetching file info:', error);
    }
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
    <div class="App">
        <div class="info-container">
            <p v-if="selectedNode">当前选中文件为：{{ selectedNode.label }}</p>
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
.App {
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: #f0f0f0;
    padding: 20px; /* 添加一些内边距 */
}

.info-container {
    width: 90%;
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 10px 20px; /* 添加内边距 */
    margin-bottom: 10px; /* 添加下外边距 */
}

.main-container {
    display: flex;
    width: 90%;
    height: 80%;
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
