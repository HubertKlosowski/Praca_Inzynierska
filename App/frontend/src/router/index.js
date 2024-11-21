import { createRouter, createWebHistory } from 'vue-router'
import MainPage from "@/components/MainPage.vue";
import Account from "@/components/CreateAccount.vue";
import ModelPhases from "@/components/ModelPhases.vue";
import Login from "@/components/Login.vue";
import PrepareData from "@/components/PrepareData.vue";
import Predictions from "@/components/Predictions.vue";

const routes = [
    { path: '/', component: MainPage },
    { path: '/create_account', component: Account },
    { path: '/data', component: PrepareData },
    { path: '/models', component: ModelPhases },
    { path: '/predict', component: Predictions },
    { path: '/login', component: Login }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router