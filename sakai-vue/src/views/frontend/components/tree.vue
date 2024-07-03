<script>
import Tree from 'primevue/tree';

export default {
    components: { Tree },
    // 接收父组件的参数
    props: ['fileinfo'],
    data() {
        return {
            nodes: null
        };
    },
    watch: {
        fileinfo(newValue) {
            if (newValue) {
                console.log('Filetree received fileinfo:', newValue);
                this.nodes = newValue;
                // 在这里可以处理 fileinfo 的逻辑
            }
        }
    },
    mounted() {
        // 初始化时，将 fileinfo 传递给子组件
        console.log('fileinfo:', this.fileinfo);
        this.nodes = this.fileinfo;
    },
    methods: {
        onNodeSelect(node) {
            this.$emit('node-selected', node); // 通过 emit 传递给父组件
            console.log(node.data);
            this.$toast.add({ severity: 'success', summary: 'Node Selected', detail: node.label, life: 3000 });
        },
        onNodeUnselect(node) {
            this.$toast.add({ severity: 'warn', summary: 'Node Unselected', detail: node.label, life: 3000 });
        },
        onNodeExpand(node) {
            this.$toast.add({ severity: 'info', summary: 'Node Expanded', detail: node.label, life: 3000 });
        },
        onNodeCollapse(node) {
            this.$toast.add({ severity: 'error', summary: 'Node Collapsed', detail: node.label, life: 3000 });
        }
    }
};
</script>

<template>
    <div class="filetree-container">
        <div class="card flex justify-content-center filetree-content">
            <Toast />
            <Tree
                v-model:selectionKeys="selectKey"
                :value="nodes"
                selectionMode="single"
                :metaKeySelection="false"
                @nodeSelect="onNodeSelect"
                @nodeUnselect="onNodeUnselect"
                @nodeExpand="onNodeExpand"
                @nodeCollapse="onNodeCollapse"
                class="w-full md:w-30rem"
            ></Tree>
        </div>
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
