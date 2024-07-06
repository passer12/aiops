<script setup>
import { ref, onMounted } from 'vue';
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

onMounted(() => {
    // countryService.getCountries().then((data) => (autoValue.value = data));
});
const handleSubmit = () => {
    console.log('提交被点击');
    if(!radioValue){
      ale
    }
    const form_data = {
        api_id: 1,
        api_secret: 1,
        api_key: 1,
        version: radioValue.value,
        max_token: sliderValue.value,
        temperature: tam_sliderValue.value
    };
    console.log(form_data);
};

// Spark Lite（传1.1）, Spark V20（传2.1）, Spark Pro（传3.1）, Spark Max（传值3.5）, Spark Ultra（传值4.0）
</script>
<template>
    <div class="grid p-fluid">
        <div class="col-12 md:col-6">
            <div class="card">
                <form @submit.prevent="handleSubmit">
                    <h5>模型版本</h5>
                    <div class="grid">
                        <div class="col-12 md:col-4">
                            <div class="field-radiobutton mb-0">
                                <RadioButton id="option1" name="option" value="1" v-model="radioValue" />
                                <label for="option1">Spark Lite</label>
                            </div>
                        </div>
                        <div class="col-12 md:col-4">
                            <div class="field-radiobutton mb-0">
                                <RadioButton id="option2" name="option" value="2" v-model="radioValue" />
                                <label for="option2">Spark V2.0</label>
                            </div>
                        </div>
                        <div class="col-12 md:col-4">
                            <div class="field-radiobutton mb-0">
                                <RadioButton id="option3" name="option" value="3" v-model="radioValue" />
                                <label for="option3">Spark Pro</label>
                            </div>
                        </div>
                        <div class="col-12 md:col-4">
                            <div class="field-radiobutton mb-0">
                                <RadioButton id="option4" name="option" value="4" v-model="radioValue" />
                                <label for="option4">Spark Max</label>
                            </div>
                        </div>
                        <div class="col-12 md:col-4">
                            <div class="field-radiobutton mb-0">
                                <RadioButton id="option5" name="option" value="5" v-model="radioValue" />
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
