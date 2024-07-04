<script setup>
import { onMounted, ref, watch } from 'vue';
import { ProductService } from '@/service/ProductService';
import { useLayout } from '@/layout/composables/layout';
import Breadcrumb from 'primevue/breadcrumb';

import Rating_tag from '@/views/utilities/rating_tag.vue';
import Evaluate from '@/views/frontend/Evaluate.vue';
const { isDarkTheme } = useLayout();
const status = ref(null);
status.value = { repo_num: 10 };
const overallRates = ref([
    { label: '可读性评分', value: 0.85 },
    { label: '性能评分', value: 0.75 },
    { label: '可用性评分', value: 0.65 },
    { label: '安全性评分', value: 0.55 },
    { label: '可维护性评分', value: 0.3 }
]);

const lineOptions = ref(null);

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
    <!--  仅限填充作用-->
    <div hidden>{{ (items[1].label = $route.query.repo) }}</div>
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
                                    <router-link :to="{ name: 'rating_detail' }" class="block text-500 font-medium mb-3">
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
