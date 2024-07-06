<script setup>
import { FilterMatchMode } from 'primevue/api';
import { ref, onMounted, onBeforeMount } from 'vue';
import { ProductService } from '@/service/ProductService';
import { useToast } from 'primevue/usetoast';
import axios from 'axios';
// 假设你的JWT令牌存储在localStorage中
const token = localStorage.getItem('token');
// 设置默认的Authorization头，自动附带认证头
axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

const toast = useToast();

const products = ref(null);
const productDialog = ref(false);
const editProductDialog = ref(false);
const deleteProductDialog = ref(false);
const deleteProductsDialog = ref(false);
const product = ref({});
const selectedProducts = ref(null);
const dt = ref(null);
const filters = ref({});
const submitted = ref(false);

const productService = new ProductService();

onBeforeMount(() => {
    initFilters();
});
onMounted(() => {
    productService.getProducts().then((data) => (products.value = data));
});

const openNew = () => {
    product.value = {};
    submitted.value = false;
    productDialog.value = true;
};

const hideDialog = () => {
    productDialog.value = false;
    editProductDialog.value = false;
    submitted.value = false;
};

const saveProduct = () => {
    submitted.value = true;
    console.log(product.value);
    const formDate = {
        Name: product.value.name,
        Description: product.value.description,
        Link: product.value.Link,
        username: localStorage.getItem('username'),
        Owner: 1
    };
    console.log('formadata', formDate);
    axios
        .post('/api/repos/', formDate)
        .then((response) => {
            console.log(response);
            toast.add({ severity: 'success', summary: 'Successful', detail: 'Product Created', life: 3000 });
            productDialog.value = false;
            product.value = {};
        })
        .catch((error) => {
            console.log(error.response.data);
            toast.add({ severity: 'error', summary: 'Error', detail: error.response.data, life: 3000 });
        });
};

const editProduct = (editProduct) => {
    console.log(editProduct);
    product.value = { ...editProduct };
    editProductDialog.value = true;
};

const updateProduct = () => {
    submitted.value = true;
    console.log(product.value);
    const formDate = {
        Name: product.value.name,
        Description: product.value.description,
        Link: product.value.Link
    };
    axios
        .patch('/api/repos/' + product.value.RepositoryID + '/', formDate)
        .then((response) => {
            console.log(response);
            toast.add({ severity: 'success', summary: 'Successful', detail: 'Product Created', life: 3000 });
            productDialog.value = false;
            product.value = {};
            location.reload();
        })
        .catch((error) => {
            console.log(error);
            toast.add({ severity: 'error', summary: 'Error', detail: error.response.data, life: 3000 });
        });
};
const confirmDeleteProduct = (editProduct) => {
    product.value = editProduct;
    console.log(editProduct);
    deleteProductDialog.value = true;
};

const deleteProduct = () => {
    console.log(product.value.RepositoryID);
    axios
        .delete('/api/repos/' + product.value.RepositoryID + '/')
        .then((response) => {
            console.log(response);
            toast.add({ severity: 'success', summary: 'Successful', detail: '成功删除', life: 3000 });
        })
        .catch((error) => {
            console.log(error);
            toast.add({ severity: 'error', summary: 'Error', detail: '删除失败，请刷新重试', life: 3000 });
        });
    deleteProductDialog.value = false;
    product.value = {};
};

const exportCSV = () => {
    dt.value.exportCSV();
};

const confirmDeleteSelected = () => {
    deleteProductsDialog.value = true;
};
const deleteSelectedProducts = () => {
    console.log(selectedProducts.value);
    //写个循环
    for (let i = 0; i < selectedProducts.value.length; i++) {
        console.log(selectedProducts.value[i].RepositoryID);
        axios
            .delete('/api/repos/' + selectedProducts.value[i].RepositoryID + '/')
            .then((response) => {
                console.log(response);
            })
            .catch((error) => {
                console.log(error);
            });
    }
    deleteProductsDialog.value = false;
    selectedProducts.value = null;
    toast.add({ severity: 'success', summary: 'Successful', detail: 'Products Deleted', life: 3000 });
};

const initFilters = () => {
    filters.value = {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS }
    };
};
</script>

<template>
    <div class="grid">
        <div class="col-12">
            <div class="card">
                <Toolbar class="mb-4">
                    <template v-slot:start>
                        <div class="my-2">
                            <Button label="New" icon="pi pi-plus" class="mr-2" severity="success" @click="openNew" />
                            <Button label="Delete" icon="pi pi-trash" severity="danger" @click="confirmDeleteSelected" :disabled="!selectedProducts || !selectedProducts.length" />
                        </div>
                    </template>

                    <template v-slot:end>
                        <FileUpload mode="basic" accept="image/*" :maxFileSize="1000000" label="Import" chooseLabel="Import" class="mr-2 inline-block" />
                        <Button label="Export" icon="pi pi-upload" severity="help" @click="exportCSV($event)" />
                    </template>
                </Toolbar>

                <DataTable
                    ref="dt"
                    :value="products"
                    v-model:selection="selectedProducts"
                    dataKey="Name"
                    :paginator="true"
                    :rows="10"
                    :filters="filters"
                    paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                    :rowsPerPageOptions="[5, 10, 25]"
                    currentPageReportTemplate="Showing {first} to {last} of {totalRecords} repos"
                >
                    <template #header>
                        <div class="flex flex-column md:flex-row md:justify-content-between md:align-items-center">
                            <h5 class="m-0">Manage Products</h5>
                            <IconField iconPosition="left" class="block mt-2 md:mt-0">
                                <InputIcon class="pi pi-search" />
                                <InputText class="w-full sm:w-auto" v-model="filters['global'].value" placeholder="Search..." />
                            </IconField>
                        </div>
                    </template>

                    <Column selectionMode="multiple" headerStyle="width: 3rem"></Column>
                    <Column field="Name" header="Name" :sortable="true" headerStyle="width:14%; min-width:10rem;">
                        <template #body="slotProps">
                            <span class="p-column-title">name</span>
                            {{ slotProps.data.Name }}
                        </template>
                    </Column>
                    <Column field="Description" header="description" :sortable="true" headerStyle="width:14%; min-width:10rem;">
                        <template #body="slotProps">
                            <span class="p-column-title">description</span>
                            {{ slotProps.data.Description }}
                        </template>
                    </Column>
                    <Column field="url" header="url" :sortable="true" headerStyle="width:14%; min-width:10rem;">
                        <template #body="slotProps">
                            <span class="p-column-title">Url</span>
                            {{ slotProps.data.Link }}
                        </template>
                    </Column>
                    <Column headerStyle="min-width:10rem;">
                        <template #body="slotProps">
                            <Button icon="pi pi-pencil" class="mr-2" severity="success" rounded @click="editProduct(slotProps.data)" />
                            <Button icon="pi pi-trash" class="mt-2" severity="warning" rounded @click="confirmDeleteProduct(slotProps.data)" />
                        </template>
                    </Column>
                </DataTable>

                <Dialog v-model:visible="productDialog" :style="{ width: '450px' }" header="Product Details" :modal="true" class="p-fluid">
                    <!--                    <img :src="'/demo/images/product/' + product.image" :alt="product.image" v-if="product.image" width="150" class="mt-0 mx-auto mb-5 block shadow-2" />-->
                    <div class="field">
                        <label for="name">Name</label>
                        <InputText id="name" v-model.trim="product.name" required="true" autofocus :invalid="submitted && !product.name" />
                        <small class="p-invalid" v-if="submitted && !product.name">Name is required.</small>
                    </div>
                    <div class="field">
                        <label for="description">Description</label>
                        <Textarea id="description" v-model="product.description" required="true" rows="3" cols="20" />
                    </div>

                    <div class="field">
                        <label for="Link">Url link</label>
                        <Textarea id="Link" v-model="product.Link" required="true" rows="3" cols="20" />
                    </div>
                    <template #footer>
                        <Button label="Cancel" icon="pi pi-times" text="" @click="hideDialog" />
                        <Button label="Save" icon="pi pi-check" text="" @click="saveProduct" />
                    </template>
                </Dialog>

                <Dialog v-model:visible="editProductDialog" :style="{ width: '450px' }" header="Product Details" :modal="true" class="p-fluid">
                    <!--                    <img :src="'/demo/images/product/' + product.image" :alt="product.image" v-if="product.image" width="150" class="mt-0 mx-auto mb-5 block shadow-2" />-->
                    <div class="field">
                        <label for="name">Name</label>
                        <InputText id="name" v-model.trim="product.name" required="true" autofocus :invalid="submitted && !product.name" />
                        <small class="p-invalid" v-if="submitted && !product.name">Name is required.</small>
                    </div>
                    <div class="field">
                        <label for="description">Description</label>
                        <Textarea id="description" v-model="product.description" required="true" rows="3" cols="20" />
                    </div>

                    <div class="field">
                        <label for="Link">Url link</label>
                        <Textarea id="Link" v-model="product.Link" required="true" rows="3" cols="20" />
                    </div>
                    <template #footer>
                        <Button label="Cancel" icon="pi pi-times" text="" @click="hideDialog" />
                        <Button label="Save" icon="pi pi-check" text="" @click="updateProduct" />
                    </template>
                </Dialog>

                <Dialog v-model:visible="deleteProductDialog" :style="{ width: '450px' }" header="Confirm" :modal="true">
                    <div class="flex align-items-center justify-content-center">
                        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
                        <span v-if="product"
                            >Are you sure you want to delete <b>{{ product.name }}</b
                            >?</span
                        >
                    </div>
                    <template #footer>
                        <Button label="No" icon="pi pi-times" text @click="deleteProductDialog = false" />
                        <Button label="Yes" icon="pi pi-check" text @click="deleteProduct" />
                    </template>
                </Dialog>

                <Dialog v-model:visible="deleteProductsDialog" :style="{ width: '450px' }" header="Confirm" :modal="true">
                    <div class="flex align-items-center justify-content-center">
                        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
                        <span v-if="product">Are you sure you want to delete the selected repos?</span>
                    </div>
                    <template #footer>
                        <Button label="No" icon="pi pi-times" text @click="deleteProductsDialog = false" />
                        <Button label="Yes" icon="pi pi-check" text @click="deleteSelectedProducts" />
                    </template>
                </Dialog>
            </div>
        </div>
    </div>
</template>
