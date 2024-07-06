<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios';
import { useToast } from 'primevue/usetoast';
import Avatar from 'primevue/avatar';
import { ProductService } from '@/service/ProductService';
import Avatar_upload from '@/views/pages/user/avatar_upload.vue';
import Repolist from '@/views/pages/repo/Repolist.vue';
const productService = new ProductService();

const toast = useToast();

// 假设你的JWT令牌存储在localStorage中
const token = localStorage.getItem('token');
// 设置默认的Authorization头，自动附带认证头
axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

const userprofile = ref({
    name: '',
    email: '',
    description: '',
    link: ''
});
const userprofile_copy = ref({});
onMounted(() => {
    productService.getProfile().then((data) => {
        userprofile.value = data;
    });
});

const editable = ref(false);
const avatar_upload_visible = ref(false);
const showAvatarUploadDialog = () => {
    avatar_upload_visible.value = true;
};

const editProfile = () => {
    userprofile_copy.value = JSON.parse(JSON.stringify(userprofile.value));
    editable.value = true;
};

const hideDialog = () => {
    editable.value = false;
};

const saveProfile = () => {
    // userprofile.value = JSON.parse(JSON.stringify(userprofile_copy.value));
    // 后端发送请求
    // 更新userprofile
    console.log(userprofile_copy.value);
    const formDate = {
        email: userprofile_copy.value.email,
        description: userprofile_copy.value.description,
        link: userprofile_copy.value.link,
        access_token: userprofile_copy.value.access_token
    };
    axios
        .patch('/api/profile/', formDate)
        .then((response) => {
            console.log(response);
            toast.add({ severity: 'success', summary: 'Successful', detail: 'Product Created', life: 3000 });
            editable.value = false;
            userprofile.value = JSON.parse(JSON.stringify(userprofile_copy.value));
        })
        .catch((error) => {
            console.log(error.response.data);
            toast.add({ severity: 'error', summary: 'Error', detail: error.response.data, life: 3000 });
        });
};
</script>
<!--//https://primefaces.org/cdn/primevue/images/usercard.png-->
<template>
    <div class="container">
        <div class="left-part">
            <Card style="width: 90%; overflow: hidden">
                <template #header>
                    <div class="avatar-container">
                        <div class="avatar-wrapper">
                            <Avatar :image="userprofile.avatar" class="avatar" size="normal" shape="circle" />
                        </div>
                        <Button label="改变头像" icon="pi pi-pencil" class="p-button-rounded p-button-text" @click="showAvatarUploadDialog" />
                    </div>
                </template>
                <template #title>{{ userprofile.name }}</template>
                <template #subtitle>{{ userprofile.email }}</template>
                <template #content>
                    <p class="m-0">
                        {{ userprofile.description }}
                    </p>

                    <p class="m-0">
                        {{ userprofile.link }}
                    </p>
                </template>
                <template #footer>
                    <div class="flex gap-4 mt-1">
                        <Button label="edit Profile" @click="editProfile"> </Button>
                    </div>
                </template>
            </Card>
        </div>
        <div class="right-part">
            <Repolist></Repolist>
        </div>
    </div>

    <Dialog v-model:visible="editable" :style="{ width: '450px' }" header="user Profile" :modal="true" class="p-fluid">
        <!--      <img :src="'/demo/images/product/' + product.image" :alt="product.image" v-if="product.image" width="150" class="mt-0 mx-auto mb-5 block shadow-2" />-->
        <div class="field">
            <label for="name">email</label>
            <InputText id="name" v-model.trim="userprofile_copy.email" required="true" autofocus :invalid="!userprofile_copy.email" />
            <small class="p-invalid" v-if="!userprofile_copy.email">email is required.</small>
        </div>
        <div class="field">
            <label for="description">description</label>
            <Textarea id="description" v-model="userprofile_copy.description" required="true" rows="3" cols="20" />
        </div>

        <div class="field">
            <label for="Link">Url link</label>
            <Textarea id="Link" v-model="userprofile_copy.link" required="true" rows="3" cols="20" />
        </div>
        <div class="field">
            <label for="Token">github token</label>
            <!--            <Password id="Token" v-model="userprofile_copy.access_token" required="true" rows="3" cols="20" />-->
            <Textarea id="Token" v-model="userprofile_copy.access_token" required="true" rows="3" cols="20" />
        </div>
        <template #footer>
            <Button label="Cancel" icon="pi pi-times" text="" @click="hideDialog" />
            <Button label="Save" icon="pi pi-check" text="" @click="saveProfile" />
        </template>
    </Dialog>
    <Dialog v-model:visible="avatar_upload_visible" :style="{ width: '70%' }" header="头像上传" :modal="true">
        <Avatar_upload></Avatar_upload>
    </Dialog>
</template>

<style>
.container {
    display: flex;
}

.left-part {
    flex: 0 0 30%; /* 占据 30% 的宽度 */
}

.right-part {
    flex: 1; /* 占据剩余的 70% 宽度 */
}

.avatar-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 20px; /* Add top margin to create space above */
}

.avatar-wrapper {
    width: 60%;
    padding-top: 60%; /* Maintain aspect ratio */
    position: relative;
    border-radius: 50%;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
}

.avatar {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover; /* Ensure the image covers the entire area */
    object-position: center; /* Center the image */
    border-radius: 50%; /* Make the avatar circular */
    display: block;
    background-color: #f0f0f0; /* Fallback background color */
}

button {
    margin-top: 10px; /* Space between avatar and button */
}
</style>
