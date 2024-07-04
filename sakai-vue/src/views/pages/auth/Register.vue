<script setup>
import { useLayout } from '@/layout/composables/layout';
import { ref, computed } from 'vue';
import AppConfig from '@/layout/AppConfig.vue';
import axios from 'axios';

const { layoutConfig } = useLayout();
const username = ref('');
const password = ref('');
const checked = ref(false);
const re_password = ref('');

const logoUrl = computed(() => {
    return `/layout/images/${layoutConfig.darkTheme.value ? 'logo-white' : 'logo-dark'}.svg`;
});

const register_send = () => {
    if (password.value !== re_password.value) {
        alert('两次密码输入不同');
        return;
    }

    const formDate = {
        username: username.value,
        password: password.value,
        re_password: re_password.value
    };

    console.log(formDate);
    axios
        .post('/api/users/', formDate)
        .then(function (response) {
            console.log(response);
            new_user_profile();
            window.location.href = '/auth/login';
        })
        .catch(function (error) {
            console.log(error);
            let errorMessages = [];
            let error_data = error.response.data;
            for (let key in error_data) {
                if (error_data.hasOwnProperty(key)) {
                    errorMessages.push(`${key}: ${error_data[key].join(", ")}`);
                }
            }
            alert(errorMessages.join("\n"));
        });
};
</script>

<template>
    <div class="surface-ground flex align-items-center justify-content-center min-h-screen min-w-screen overflow-hidden">
        <div class="flex flex-column align-items-center justify-content-center">
            <img :src="logoUrl" alt="Sakai logo" class="mb-5 w-6rem flex-shrink-0" />
            <div style="border-radius: 56px; padding: 0.3rem; background: linear-gradient(180deg, var(--primary-color) 10%, rgba(33, 150, 243, 0) 30%)">
                <div class="w-full surface-card py-8 px-5 sm:px-8" style="border-radius: 53px">
                    <div class="text-center mb-5">
                        <!--                        <img src="/demo/images/login/avatar.png" alt="Image" height="50" class="mb-3" />-->
                        <div class="text-900 text-3xl font-medium mb-3">Welcome, {{ username ? username : 'New user' }}</div>
                        <span class="text-600 font-medium">Sign up to continue</span>
                    </div>

                    <div>
                        <label for="username1" class="block text-900 text-xl font-medium mb-2">Username</label>
                        <InputText id="username1" type="text" placeholder="username" class="w-full md:w-30rem mb-5" style="padding: 1rem" v-model="username" />

                        <label for="password1 " class="block text-900 font-medium text-xl mb-2">Password</label>
                        <Password id="password1" v-model="password" placeholder="Password" :toggleMask="true" class="w-full mb-3" inputClass="w-full" :inputStyle="{ padding: '1rem' }"></Password>

                        <label for="password2" class="block text-900 font-medium text-xl mb-2">Re input password</label>
                        <Password id="password2" v-model="re_password" placeholder="Password" :toggleMask="true" class="w-full mb-3" inputClass="w-full" :inputStyle="{ padding: '1rem' }"></Password>

                        <div class="flex align-items-center justify-content-between mb-5 gap-5">
                            <div class="flex align-items-center">
                                <Checkbox v-model="checked" id="rememberme1" binary class="mr-2"></Checkbox>
                                <label for="rememberme1">Remember me</label>
                            </div>
                            <a class="font-medium no-underline ml-2 text-right cursor-pointer" style="color: var(--primary-color)">Forgot password?</a>
                        </div>
                        <Button label="Sign up" class="w-full p-3 text-xl" @click="register_send()"></Button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <AppConfig simple />
</template>

<style scoped>
.pi-eye {
    transform: scale(1.6);
    margin-right: 1rem;
}

.pi-eye-slash {
    transform: scale(1.6);
    margin-right: 1rem;
}
</style>
