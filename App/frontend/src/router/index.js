import { createRouter, createWebHistory } from 'vue-router'
import { inject } from 'vue'

import UserForm from '@/components/LoginForm.vue'
import ForgotPassword from '@/components/ForgotPassword.vue'
import Details from '@/components/Details.vue'
import CreateAccount from '@/components/CreateAccount.vue'
import MainPage from '@/components/MainPage.vue'
import Submission from '@/components/Submission.vue'
import UserProfile from '@/components/UserProfile.vue'
import SubmitPanel from '@/components/SubmitPanel.vue'
import ChatPanel from '@/components/ChatPanel.vue'
import StatsPanel from '@/components/StatsPanel.vue'


const routes = [
    { path: '/', component: MainPage },
    { path: '/login', component: UserForm, },
    { path: '/details', component: Details },
    { path: '/forgot_password', component: ForgotPassword },
    { path: '/create_account', component: CreateAccount },
    { path: '/submissions', component: Submission,
        children: [
            {
                path: 'submit',
                component: SubmitPanel
            },
            {
                path: 'chat',
                component: ChatPanel
            },
            {
                path: 'stats',
                component: StatsPanel
            }
        ]
    },
    { path: '/profile', component: UserProfile }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach(async (to, from) => {
    const $cookies = inject('$cookies')
    if ((to.path === '/profile' || to.path === '/submissions') && !$cookies.get('user')) {
        return false
    } else if (to.path === '/submissions/chat' && $cookies.get('user')['usertype'] === 0) {
        return false
    }
})

export default router