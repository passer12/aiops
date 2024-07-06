<script setup>
import { ref, onMounted } from 'vue';
import { useToast } from 'primevue/usetoast';

const toast = useToast();
import axios from 'axios';
// 假设你的JWT令牌存储在localStorage中
const token = localStorage.getItem('token');

// 设置默认的Authorization头，自动附带认证头
axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

const sliderValue = ref(4096);
const maxValue = ref(8192);

const tam_sliderValue = ref(0.5);
const tam_maxValue = ref(1.0);
const radioValue = ref(null);
const app_id = ref('e8bd2492');
const api_secret = ref('MGY1MjIzMDk1MTQ4Y2U1YzUxMWI5Yzk1');
const api_key = ref('28b98e55ec8e83daddf1e591952e2614');
onMounted(() => {
    // countryService.getCountries().then((data) => (autoValue.value = data));
});
const handleSubmit = () => {
    console.log('提交被点击');
    if (!radioValue.value) {
        alert('请选择模型版本');
        return false;
    }

    const form_data = {
        app_id: app_id.value,
        api_secret: api_secret.value,
        api_key: api_key.value,
        version: radioValue.value,
        max_tokens: sliderValue.value,
        temperature: tam_sliderValue.value
    };
    console.log(form_data);
    axios
        .get('/api/spark/update_aiOps_config/', { params: form_data })
        .then((response) => {
            console.log(response);
            toast.add({ severity: 'success', summary: '成功', detail: '配置已更新', life: 3000 });
        })
        .catch((error) => {
            console.error('There was an error with the GET request:', error);
            toast.add({ severity: 'error', summary: '失败', detail: error, life: 3000 });
        });
};

// Spark Lite（传1.1）, Spark V20（传2.1）, Spark Pro（传3.1）, Spark Max（传值3.5）, Spark Ultra（传值4.0）
</script>
<template>
    <div class="grid p-fluid">
        <div class="col-12 md:col-6">
            <div class="card">
                <form @submit.prevent="handleSubmit">
                    <div class="card flex flex-wrap gap-4">
                        <div class="flex-auto">
                            <FloatLabel>
                                <InputText id="app_id" v-model="app_id" />
                                <label for="app_id">App_id</label>
                            </FloatLabel>
                        </div>
                        <div class="flex-auto">
                            <FloatLabel>
                                <InputText id="api_secret" v-model="api_secret" />
                                <label for="api_secret">api_secret</label>
                            </FloatLabel>
                        </div>
                        <div class="flex-auto">
                            <FloatLabel>
                                <InputText id="api_key" v-model="api_key" />
                                <label for="api_key">api_key</label>
                            </FloatLabel>
                        </div>
                    </div>

                    <h5>模型版本</h5>
                    <div class="grid">
                        <div class="col-12 md:col-4">
                            <div class="field-radiobutton mb-0">
                                <RadioButton id="option1" name="option" value="1.1" v-model="radioValue" />
                                <label for="option1">Spark Lite</label>
                            </div>
                        </div>
                        <div class="col-12 md:col-4">
                            <div class="field-radiobutton mb-0">
                                <RadioButton id="option2" name="option" value="2.0" v-model="radioValue" />
                                <label for="option2">Spark V2.0</label>
                            </div>
                        </div>
                        <div class="col-12 md:col-4">
                            <div class="field-radiobutton mb-0">
                                <RadioButton id="option3" name="option" value="3.1" v-model="radioValue" />
                                <label for="option3">Spark Pro</label>
                            </div>
                        </div>
                        <div class="col-12 md:col-4">
                            <div class="field-radiobutton mb-0">
                                <RadioButton id="option4" name="option" value="3.5" v-model="radioValue" />
                                <label for="option4">Spark Max</label>
                            </div>
                        </div>
                        <div class="col-12 md:col-4">
                            <div class="field-radiobutton mb-0">
                                <RadioButton id="option5" name="option" value="4.0" v-model="radioValue" />
                                <label for="option5">Spark Ultra</label>
                            </div>
                        </div>
                    </div>
                    <div class="col-12">
                        <h5>max token</h5>
                        <InputText v-model.number="sliderValue" />
                        <Slider v-model="sliderValue" :max="maxValue" />
                    </div>

                    <div class="col-12">
                        <h5>temperature</h5>
                        <InputText v-model.number="tam_sliderValue" />
                        <Slider v-model="tam_sliderValue" :max="tam_maxValue" :step="tam_maxValue / 100" />
                    </div>
                    <div class="col-12">
                        <Button type="submit" label="提交" />
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>
