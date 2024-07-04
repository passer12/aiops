<script setup>
import axios from 'axios';
import { ref } from 'vue';
import {useToast } from 'primevue/usetoast';
const toast = useToast();

const customBase64Uploader = async (event) => {
    const file = event.files[0];
    const formData = new FormData();
    formData.append('avatar', file);
    const token = localStorage.getItem('token');
    // console.log(event.url);
    axios
        .post('/api/profile/upload_avatar/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
                Authorization: `Bearer ${token}`
            }
        })
        .then((response) => {
            console.log('File uploaded successfully');
            console.log('Upload successful', response.data);
            toast.add({ severity: 'success', summary: 'Success', detail: 'Avatar uploaded successfully', life: 3000 });
            // 重新加载
            window.location.reload();
        })
        .catch((error) => {
            console.error('Error uploading file', error);
            toast.add({ severity: 'error', summary: 'Error', detail: 'Error uploading avatar', life: 3000 });
        });
};
</script>

<template>
    <div class="card flex justify-center">
        <FileUpload mode="basic" name="demo[]" url="/api/profile/upload_avatar/" accept="image/*" customUpload @uploader="customBase64Uploader" />
    </div>
</template>
