<script setup>
import { onMounted, ref, watch } from 'vue';
import { ProductService } from '@/service/ProductService';
import { useLayout } from '@/layout/composables/layout';
import Breadcrumb from 'primevue/breadcrumb';
import axios from 'axios';
const token = localStorage.getItem('token');
import Rating_tag from '@/views/sakai/utilities/rating_tag.vue';
import Evaluate from '@/views/pages/evaluation/Evaluate.vue';
const { isDarkTheme } = useLayout();
const status = ref(null);
status.value = { repo_num: 10 };

// 设置默认的Authorization头，自动附带认证头
axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

const lineOptions = ref(null);

// const repo_score = ref(null);
// const repo_url = window.localStorage.getItem('repo_url');
// const fetchFileInfo = async () => {
//     console.log('================================fetchFileInfo================================');
//     axios
//         .get('/api/spark/view_repo_json_secure/', {
//             params: {
//                 repo_url: repo_url
//             }
//         })
//         .then((response) => {
//             repo_score.value = response.data.repo_score;
//             console.log('repo_score', repo_score.value);
//         })
//         .catch((error) => {
//             console.error('Error fetching file info:', error);
//         });
// };
// onMounted(fetchFileInfo);

// const overallRates = ref([
//     { label: '可读性评分', value: repo_score.value.avg_readability },
//     { label: '性能评分', value: repo_score.value.avg_performance },
//     { label: '可用性评分', value: repo_score.value.avg_usability },
//     { label: '安全性评分', value: repo_score.value.avg_security },
//     { label: '可维护性评分', value: repo_score.value.avg_maintainability }
// ]);

import { computed } from 'vue';

const repo_score = ref(null);
const repo_url = window.localStorage.getItem('repo_url');

const fetchFileInfo = async () => {
    console.log('================================fetchFileInfo================================');
    try {
        const response = await axios.get('/api/spark/view_repo_json_secure/', {
            params: { repo_url: repo_url }
        });
        repo_score.value = response.data.repo_score;
        console.log('repo_score', repo_score.value);
    } catch (error) {
        console.error('Error fetching file info:', error);
    }
};

onMounted(fetchFileInfo);

const overallRates = computed(() => {
    if (!repo_score.value) return [];
    
    return [
        { label: '可读性评分', value: repo_score.value.avg_readability },
        { label: '性能评分', value: repo_score.value.avg_performance },
        { label: '可用性评分', value: repo_score.value.avg_usability },
        { label: '安全性评分', value: repo_score.value.avg_security },
        { label: '可维护性评分', value: repo_score.value.avg_maintainability }
    ];
});

// const overallRates = ref([
//     { label: '可读性评分', value: 1 },
//     { label: '性能评分', value: 1 },
//     { label: '可用性评分', value: 1 },
//     { label: '安全性评分', value: 1 },
//     { label: '可维护性评分', value: 1 }
// ]);

// import { computed } from 'vue';

// // 先创建一个响应式对象来存储 file_score
// const repoScoreData = ref(null);

// // 在适当的时机（比如 onMounted 钩子中）获取并设置数据
// onMounted(() => {
//   const repoScoreData = repo_score;
// });

// // 使用计算属性创建 overallRates
// const overallRates = computed(() => {
//   if (!repoScoreData.value) return [];
  
//   return [
//     { label: '可读性评分', value: repoScoreData.value?.avg_readability },
//     { label: '性能评分', value: repoScoreData.value?.avg_performance },
//     { label: '可用性评分', value: repoScoreData.value?.avg_usability },
//     { label: '安全性评分', value: repoScoreData.value?.avg_security },
//     { label: '可维护性评分', value: repoScoreData.value?.avg_maintainability }
//   ];
// });


onMounted(() => {
    // productService.getProducts().then((data) => (products.value = data));
});
const applyLightTheme = () => {
    lineOptions.value = {
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
    };
};

const applyDarkTheme = () => {
    lineOptions.value = {
        plugins: {
            legend: {
                labels: {
                    color: '#ebedef'
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    color: '#ebedef'
                },
                grid: {
                    color: 'rgba(160, 167, 181, .3)'
                }
            },
            y: {
                ticks: {
                    color: '#ebedef'
                },
                grid: {
                    color: 'rgba(160, 167, 181, .3)'
                }
            }
        }
    };
};

watch(
    isDarkTheme,
    (val) => {
        if (val) {
            applyDarkTheme();
        } else {
            applyLightTheme();
        }
    },
    { immediate: true }
);

// breadcrumb区域
const home = ref({
    icon: 'pi pi-home',
    to: '/pages/profile'
});
const reponame = ref(window.localStorage.getItem('repo_name') ? window.localStorage.getItem('repo_name') : 'examplerepo');
const items = ref([{ label: window.localStorage.getItem('username'), url: '/pages/profile' }, { label: reponame }]); //
</script>
<template>
    <!-- 仅限填充作用，逆天代码 -->
    <div hidden>{{ (items[1].label = $route.query.repo ? $route.query.repo : items[1].label) }}</div>
    <Breadcrumb :home="home" :model="items" />
    <p></p>
    <div class="card">
        <TabView>
            <TabPanel key="rating" header="总体评分">
                <div class="grid">
                    <div class="col-12 md:col-4 lg:col-4 xl:col-4" v-for="(rate, index) in overallRates" :key="index">
                        <div class="card mb-0">
                            <div class="flex justify-content-between mb-3">
                                <div>
                                    <router-link  class="block text-500 font-medium mb-3">
                                        {{ rate.label }}
                                    </router-link>
                                    <div class="text-900 font-medium text-xl">{{ rate.value }}</div>
                                </div>
                                <div class="flex align-items-center justify-content-center bg-blue-100 border-round" style="width: 2.5rem; height: 2.5rem">
                                    <i class="pi pi-shopping-cart text-blue-500 text-xl"></i>
                                </div>
                            </div>
                            <Rating_tag :rate="rate.value"></Rating_tag>
                        </div>
                    </div>
                </div>
            </TabPanel>
            <TabPanel key="fileinfo" header="文件评估">
                <Evaluate></Evaluate>
            </TabPanel>
        </TabView>
    </div>
</template>

<style lang="scss" scoped>
.hidden {
    display: none;
}
</style>
