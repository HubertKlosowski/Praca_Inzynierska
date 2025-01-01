import {createRouter, createWebHistory} from "vue-router";
import MainPage from "@/components/MainPage.vue";
import Account from "@/components/Account.vue";
import Phases from "@/components/Phases.vue";
import Login from "@/components/Login.vue";
import MainPredictions from "@/components/MainPredictions.vue";
import {inject, reactive} from "vue";
import CreateAccount from "@/components/CreateAccount.vue";
import _ from "lodash"
import UpdateAccount from "@/components/UpdateAccount.vue";
import CreateFile from "@/components/CreateFile.vue";
import DeleteAccount from "@/components/DeleteAccount.vue";
import AccountLimits from "@/components/AccountLimits.vue";


const routes = [
    { path: '/', component: MainPage },
    { path: '/create_account', component: CreateAccount },
    { path: '/phases', component: Phases },
    { path: '/predict', component: MainPredictions },
    { path: '/login', component: Login },
    { path: '/profile', component: Account },
    { path: '/update', component: UpdateAccount },
    { path: '/create_file', component: CreateFile },
    { path: '/delete', component: DeleteAccount },
    { path: '/limits', component: AccountLimits }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach(async (to, from) => {
    const $cookies = inject('$cookies')
    const user = reactive(JSON.parse(localStorage.getItem('user')))

    if (from.path === '/profile' && to.path === '/predict') {
        return true
    } else if ((from.path === '/delete' || from.path === '/update') && to.path === '/profile') {
        return true
    } else if (!$cookies.isKey('made_submission') && to.path === '/predict' && _.isEmpty(user)) {
        return false
    } else if ((to.path === '/profile' || to.path === '/update') && _.isEmpty(user)) {
        return false
    } else if (!_.isEmpty(user) && (to.path === '/login' || to.path === '/create_account')) {
        return false
    }
})

export default router