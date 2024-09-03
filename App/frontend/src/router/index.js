import { createRouter, createWebHistory } from 'vue-router'

import UserForm from '@/components/LoginForm.vue'
import ForgotPassword from '@/components/ForgotPassword.vue'
import Details from '@/components/Details.vue'
import CreateAccount from '@/components/CreateAccount.vue'
import MainPage from '@/components/MainPage.vue'
import Submission from '@/components/Submission.vue'

const routes = [
    { path: '/', component: MainPage },
    { path: '/login', component: UserForm },
    { path: '/details', component: Details },
    { path: '/forgot_password', component: ForgotPassword },
    { path: '/create_account', component: CreateAccount },
    { path: '/submissions', component: Submission }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router