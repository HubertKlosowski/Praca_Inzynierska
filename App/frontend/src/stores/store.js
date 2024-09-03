import { defineStore } from 'pinia'
import { ref } from 'vue'


export const useUserData = defineStore('user', () => {
    const user_obj = ref({
        'name': '',
        'email': '',
        'username': '',
        'usertype': 0
    })

    const updateUser = (data) => {
        user_obj.value.name = data.name
        user_obj.value.email = data.email
        user_obj.value.username = data.username
        user_obj.value.usertype = data.usertype
    }

    return { user_obj, updateUser }
})