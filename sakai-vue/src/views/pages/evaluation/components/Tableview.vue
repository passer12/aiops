<script>
import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';

export default {
    components: { TabView, TabPanel },
    props: ['selectNode'],
    watch: {
        selectNode(newValue) {
            if (newValue) {
                console.log('选中文件更改:', newValue);
                // 这里可以更新 tabs 的内容
                this.tabs = newValue.data;
                // this.tabs = newValue;
                // 在这里可以处理 fileinfo 的逻辑
            }
        }
    },
    data() {
        return {
            tabs: [
                { title: '文件信息', content: '请选择文件' },
                { title: '代码审查', content: '请选择文件' },
                { title: '代码优化', content: '请选择文件' },
                { title: '代码分析', content: '请选择文件' }
            ]
        };
    }
};
</script>

<template>
    <div class="card">
        <TabView>
            <TabPanel v-for="tab in tabs" :key="tab.title" :header="tab.title">
                <!--                <pre class="m-0">{{ tab.content }}</pre> 文本中带有换行符-->
                <p class="m-0">{{ tab.content }}</p>
            </TabPanel>
        </TabView>
    </div>
</template>

<style scoped>
.filetree-container {
    position: relative;
    width: 100%; /* Adjust as needed */
    height: 100%; /* 400px Fixed height for the container */
    border: 1px solid #ccc; /* Optional: add border for clarity */
    overflow: hidden; /* Hide the scrollbar initially */
}

.filetree-content {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    overflow-y: auto; /* Add vertical scrollbar */
    padding-right: 15px; /* Space for the custom scrollbar */
}

/* Custom scrollbar styles */
.filetree-content::-webkit-scrollbar {
    width: 8px; /* Width of the scrollbar */
}

.filetree-content::-webkit-scrollbar-thumb {
    background-color: rgba(0, 0, 0, 0.5); /* Color of the scrollbar thumb */
    border-radius: 4px; /* Rounded corners */
}

.filetree-content::-webkit-scrollbar-track {
    background-color: rgba(0, 0, 0, 0.1); /* Color of the scrollbar track */
    border-radius: 4px; /* Rounded corners */
}
</style>
