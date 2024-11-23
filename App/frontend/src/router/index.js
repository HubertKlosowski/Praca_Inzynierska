import { createRouter, createWebHistory } from 'vue-router'
import MainPage from "@/components/MainPage.vue";
import Account from "@/components/CreateAccount.vue";
import Phases from "@/components/Phases.vue";
import Login from "@/components/Login.vue";
import MainPredictions from "@/components/MainPredictions.vue";
import Errors from "@/components/Errors.vue";

const routes = [
    { path: '/', component: MainPage },
    { path: '/create_account', component: Account },
    { path: '/phases', component: Phases },
    { path: '/predict', component: MainPredictions },
    { path: '/login', component: Login },
    { path: '/predict_errors', component: Errors }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router