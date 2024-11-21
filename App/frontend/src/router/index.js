import { createRouter, createWebHistory } from 'vue-router'
import MainPage from "@/components/MainPage.vue";
import Account from "@/components/CreateAccount.vue";
import Phases from "@/components/Phases.vue";
import Login from "@/components/Login.vue";
import Predictions from "@/components/Predictions.vue";

const routes = [
    { path: '/', component: MainPage },
    { path: '/create_account', component: Account },
    { path: '/phases', component: Phases },
    { path: '/predict', component: Predictions },
    { path: '/login', component: Login }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router