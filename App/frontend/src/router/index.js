import { createRouter, createWebHistory } from 'vue-router'
import MainPage from "@/components/MainPage.vue";
import Account from "@/components/Account.vue";
import Phases from "@/components/Phases.vue";
import Login from "@/components/Login.vue";
import MainPredictions from "@/components/MainPredictions.vue";
import {inject, ref} from "vue";
import CreateAccount from "@/components/CreateAccount.vue";
import _ from "lodash"


const routes = [
    { path: '/', component: MainPage },
    { path: '/create_account', component: CreateAccount },
    { path: '/phases', component: Phases },
    { path: '/predict', component: MainPredictions },
    { path: '/login', component: Login },
    { path: '/profile', component: Account }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach(async (to, from) => {
    const $cookies = inject('$cookies')
    const user = ref(JSON.parse(localStorage.getItem('user')))

    if (!$cookies.isKey('made_submission') && to.path === '/predict') {
        return false
    } else if (to.path === '/profile' && _.isEmpty(user.value)) {
        return false
    }
})

export default router