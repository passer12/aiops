import { createRouter, createWebHistory } from 'vue-router';
import AppLayout from '@/layout/AppLayout.vue';
import axios from 'axios';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/dashboard',
            component: AppLayout,
            meta: { requiresAuth: true },
            children: [
                {
                    path: '/dashboard',
                    name: 'dashboard',
                    component: () => import('@/views/pages/dashboard.vue')
                },
                {
                    path: '/pages/home',
                    name: 'home',
                    component: () => import('@/views/pages/evaluation/home.vue')
                },
                {
                    path: '/pages/repocrud',
                    name: 'repocrud',
                    component: () => import('@/views/pages/repo/RepoCrud.vue')
                },
                {
                    path: '/pages/repolist',
                    name: 'repolist',
                    component: () => import('@/views/pages/repo/Repolist.vue')
                },
                {
                    path: '/pages/profile',
                    name: 'profile',
                    component: () => import('@/views/pages/user/profile.vue')
                },
                {
                    path: '/pages/evaluate',
                    name: 'evaluate',
                    component: () => import('@/views/pages/evaluation/Evaluate.vue')
                },
                {
                    path: '/pages/rating_detail',
                    name: 'rating_detail',
                    component: () => import('@/views/pages/evaluation/rating_detail.vue')
                },
                {
                    path: '/pages/chat',
                    name: 'chat',
                    component: () => import('@/views/pages/Chat.vue')
                },
                {
                    path: '/pages/history',
                    name: 'history',
                    component: () => import('@/views/pages/history/history.vue')
                },
                {
                    path: '/pages/config',
                    name: 'config',
                    component: () => import('@/views/pages/config.vue')
                },
                {
                    path: '/documentation',
                    name: 'documentation',
                    component: () => import('@/views/sakai/utilities/Documentation.vue')
                }
            ]
        },
        {
            path: '/',
            name: 'landing',
            component: () => import('@/views/pages/Landing.vue')
        },
        {
            path: '/pages/notfound',
            name: 'notfound',
            component: () => import('@/views/sakai/NotFound.vue')
        },

        {
            path: '/auth/login',
            name: 'login',
            component: () => import('@/views/pages/auth/Login.vue')
        },
        {
            path: '/auth/register',
            name: 'register',
            component: () => import('@/views/pages/auth/Register.vue')
        },
        {
            path: '/auth/access',
            name: 'accessDenied',
            component: () => import('@/views/pages/auth/Access.vue')
        },
        {
            path: '/auth/error',
            name: 'error',
            component: () => import('@/views/pages/auth/Error.vue')
        }
    ]
});

// 导航守卫
// 使用 router.beforeEach 注册一个全局前置守卫，判断用户是否登陆
router.beforeEach((to, from, next) => {
    if (to.path === '/auth/login' || to.path === '/auth/register' || to.path === '/') {
        next();
    } else {
        let token = localStorage.getItem('token');

        if (token === null || token === '') {
            next('/auth/login');
        } else {
            axios
                .post('/api/jwt/verify', { token: token })

                .then((response) => {
                    if (response.status === 200) {
                        next();
                    } else {
                        alert('token已失效');
                        next('/auth/login');
                    }
                })
                .catch((error) => {
                    console.log(error);
                    alert('token已失效');
                    next('/auth/login');
                });
        }
    }
});

export default router;
