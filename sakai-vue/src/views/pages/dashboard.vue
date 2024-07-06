<script setup>
import { ref, onMounted, reactive } from 'vue';
import axios from 'axios';
// 假设你的JWT令牌存储在localStorage中
const token = localStorage.getItem('token');
// 设置默认的Authorization头，自动附带认证头
axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
const todays_history = ref(null);
const before_history = ref(null);
const username = localStorage.getItem('username');

// 初始化一个数组来存放过去一周各天的数据
const weekData = ref([0, 0, 0, 0, 0, 0, 0]); // 0: Sunday, 1: Monday, ..., 6: Saturday

// 获取当前日期和一周前的日期
const currentDate = new Date();
const oneWeekAgo = new Date();
oneWeekAgo.setDate(currentDate.getDate() - 7);

const get_history = () => {
    axios
        .get('/api/repos/history/')
        .then((response) => {
            console.log(response.data);
            todays_history.value = response.data.today;
            before_history.value = response.data.before;
            const all_histories = [todays_history.value, before_history.value];
            console.log(todays_history.value);
            //遍历todays_history
            all_histories.forEach((history) => {
                history.forEach((item) => {
                    console.log(item.action);
                    if (item.status_code >= 400) {
                        item['state'] = '失败';
                    } else {
                        item['state'] = '成功';
                    }
                    if (item.method === 'POST') {
                        item['operate'] = '创建';
                    } else if (item.method === 'PATCH') {
                        item['operate'] = '修改';
                    } else {
                        item['operate'] = '删除';
                    }
                    item['repo'] = item.payload;
                    item['user'] = username;

                    const itemDate = new Date(item.timestamp);
                    // 仅处理过去一周的数据
                    if (itemDate >= oneWeekAgo && itemDate <= currentDate) {
                        // 根据 timestamp 字段确定是哪一天
                        const dayOfWeek = itemDate.getDay(); // 0: Sunday, 1: Monday, ..., 6: Saturday

                        // 将 item 存放到对应的天中
                        weekData.value[dayOfWeek]++;
                    }
                });
            });
            console.log('weekdata', weekData.value);
        })
        .catch((error) => {
            console.error(error);
        });
};
onMounted(get_history);

const lineOptions = ref({
    plugins: {
        legend: {
            labels: {
                color: '#495057'
            }
        }
    },
    scales: {
        x: {
            ticks: {
                color: '#495057'
            },
            grid: {
                color: '#ebedef'
            }
        },
        y: {
            ticks: {
                color: '#495057'
            },
            grid: {
                color: '#ebedef'
            }
        }
    }
});

const lineData = reactive({
    labels: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
    datasets: [
        {
            label: '操作次数',
            data: weekData.value,
            fill: false,
            backgroundColor: '#00bb7e',
            borderColor: '#00bb7e',
            tension: 0.4
        }
    ]
});
</script>

<template>
    <div class="card" style="width: 50%; height: 50%">
        <h5>状态</h5>
        <Chart type="line" :data="lineData" :options="lineOptions" />
    </div>
    <div class="card" style="display: flex">
        <div class="card" style="width: 50%; height: 50%">
            <h5>今日操作记录</h5>
            <DataTable :frozen="true" :paginatorPosition="'top'" :value="todays_history" paginator :rows="5" :rowsPerPageOptions="[5, 10, 20, 50]" tableStyle="min-width: 30rem">
                <Column field="user" header="User" style="width: 25%"></Column>
                <Column field="operate" header="operation" style="width: 25%"></Column>
                <Column field="repo" header="repo" style="width: 25%"></Column>
                <Column field="state" header="state" style="width: 25%"></Column>
            </DataTable>
        </div>
        <div class="card" style="width: 50%; height: 50vh">
            <h5>历史</h5>
            <DataTable :paginatorPosition="'top'" :value="before_history" paginator :rows="5" :rowsPerPageOptions="[5, 10, 20, 50]" tableStyle="min-width: 30rem">
                <Column field="user" header="User" style="width: 25%"></Column>
                <Column field="operate" header="operation" style="width: 25%"></Column>
                <Column field="repo" header="repo" style="width: 25%"></Column>
                <Column field="state" header="state" style="width: 25%"></Column>
            </DataTable>
        </div>
    </div>
</template>
