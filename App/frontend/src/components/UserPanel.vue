<script setup>
import { inject, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import SetPassword from '@/components/SetPassword.vue'

const router = useRouter()
const $cookies = inject('$cookies')

const user_types = ['Normal', 'Pro', 'Admin']
const edit_user_data = ref(false)
const show_info = ref(false)
const name = ref('')
const username = ref('')
const email = ref('')
const password = ref('')
const info = ref('')

const updateUser = async () => {
  const user_obj = {
    name: name.value,
    email: email.value,
    username: username.value,
    password: password.value
  }
  for (const [key, value] of Object.entries(user_obj)) {
    if (value.length === 0) {
      delete user_obj[key]
    }
  }

  try {
    const to_update = await axios.patch('http://localhost:8000/api/user/update_user/' + $cookies.get('user')['id'], user_obj)
    info.value = to_update.data['success']
  } catch (error) {
    const error_response = error.response.data
    if (typeof error_response['error'] === 'string') {
      info.value = error_response['error']
    } else {
      info.value = error_response['error'].join(' ')
    }
  }

  let prev = $cookies.get('user')
  for (const [key, value] of Object.entries(user_obj)) {
    prev[key] = value
  }
  $cookies.remove('user')
  $cookies.set('user', prev)
  show_info.value = true

  await new Promise(resolve => setTimeout(resolve, 1000))
  resetInputs()

  show_info.value = false
  edit_user_data.value = false
}

const deleteUser = async () => {
  try {
    const response = await axios.delete('http://localhost:8000/api/user/delete_user/' + $cookies.get('user')['username'])
    $cookies.remove('user')
    info.value = response.data['success']
    await router.push('/')
  } catch (error) {
    const error_response = error.response.data
    if (typeof error_response['error'] === 'string') {
      info.value = error_response['error']
    } else {
      info.value = error_response['error'].join(' ')
    }
  }
}

const logout = async () => {
  if ($cookies.isKey('chat')) {
    try {
      const response = await axios.post('http://localhost:8000/api/user/save_chat', {
        user: $cookies.get('user')['id'],
        chat: $cookies.get('chat')
      })
      console.log(response)
    } catch (error) {
      console.log(error)
    }
  }
  for (const cookie_key of $cookies.keys()) {
    if ($cookies.get(cookie_key)) {
      $cookies.remove(cookie_key)
    }
  }
  await router.push('/')
}

const resetInputs = () => {
  edit_user_data.value = !edit_user_data.value
  name.value = ''
  username.value = ''
  email.value = ''
  info.value = ''
}
</script>

<template>
  <div class="container" v-if="!show_info">
    <div class="row main_row">
      <div class="image">
        <img src="@/assets/user.png" alt="Ikonka">
        <div class="create_at">
          Utworzony: {{ $cookies.get('user')['created_at'].slice(0, 10) }}
        </div>
        <div class="row">
          <button type="button" @click="edit_user_data = !edit_user_data" class="buttons" id="edit" v-show="!edit_user_data">Edytuj</button>
          <button type="button" @click="deleteUser" class="buttons" id="delete" v-show="!edit_user_data">Usuń</button>
          <button type="button" @click="logout" class="buttons" id="logout" v-show="!edit_user_data">Wyloguj</button>
          <button
              type="button"
              @click="$emit('goBack', true)" class="buttons"
              v-show="!edit_user_data && user_types[$cookies.get('user')['usertype']] === 'Admin'"
              id="manage">Zarządzaj</button>
        </div>
      </div>
      <div class="user_info" v-show="!edit_user_data">
        <div class="row user_row">
          <div class="name">
            <b>Imię</b> {{ $cookies.get('user')['name'] }}
          </div>
          <div class="username">
            <b>Nazwa użytkownika</b> {{ $cookies.get('user')['username'] }}
          </div>
        </div>
        <div class="row user_row">
          <div class="email">
            <b>Email</b> {{ $cookies.get('user')['email'] }}
          </div>
          <div class="usertype">
            <b>Typ konta</b> {{ user_types[$cookies.get('user')['usertype']] }}
          </div>
          <div class="submission_num">
            <b>Liczba prób</b> {{ $cookies.get('user')['submission_num'] }}
          </div>
        </div>
      </div>
      <div class="form" v-show="edit_user_data">
        <form @submit.prevent="updateUser">
          <div class="form_row">
            <label for="name">Imię</label>
            <input type="text" v-model="name" id="name" :placeholder="$cookies.get('user')['name']">
            <label for="username">Nazwa użytkownika</label>
            <input type="text" v-model="username" id="username" :placeholder="$cookies.get('user')['username']">
          </div>
          <div class="form_row">
            <label for="email">Email</label>
            <input type="text" v-model="email" id="email" :placeholder="$cookies.get('user')['email']">
          </div>
          <div class="form_row">
            <SetPassword @set-password="(passwd) => password = passwd"></SetPassword>
          </div>
          <div class="form_row">
            <button type="submit" class="form_buttons" id="save">Zapisz</button>
            <button type="button" class="form_buttons" id="return" @click="resetInputs">Wróć</button>
          </div>
        </form>
      </div>
    </div>
    <div class="row main_row">
      <div class="submission" v-for="n in 3">
        {{ n }}
      </div>
    </div>
  </div>
  <div class="container" v-else>
    <div
        class="info"
        :style="{ color: info.startsWith('BŁĄD') ? 'darkred' : 'darkgreen',
        display: info.length !== 0 ? 'initial' : 'none' }">
      {{ info }}
    </div>
  </div>
</template>

<style scoped>
.main_row {
  width: 100%;
  height: 50%;
}

.image {
  width: 15%;
  height: auto;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  margin: 10px;
  background-color: rgb(248, 249, 250);
  border-radius: 8px;
}

img {
  width: 150px;
  height: 100px;
}

.create_at {
  text-align: center;
}

.user_info {
  display: flex;
  flex-direction: column;
}

.user_info, .form {
  width: 75%;
}

.row {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: space-between;
  color: #2c3e50;
  padding: 10px;
}

.user_row {
  justify-content: space-evenly;
}

.user_row > * {
  background-color: rgb(248, 249, 250);
  border-radius: 8px;
  width: 45%;
  padding: 20px;
  margin: 10px;
  font-size: 1.2rem;
}

form {
  display: grid;
  grid-template-columns: 1fr 2fr;
  grid-gap: 15px;
}

.info {
  padding: 20px;
  background-color: rgb(248, 249, 250);
  border-radius: 8px;
  color: darkred;
  font-size: 1.2rem;
}

.form_row {
  display: contents;
}

.submission {
  width: 25%;
  height: 85%;
  background-color: rgb(248, 249, 250);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

label {
  margin-bottom: 4px;
  font-weight: bold;
  color: #2c3e50;
}

input {
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  font-size: 1rem;
  background-color: #ecf0f1;
  transition: border-color 0.3s;
}

button {
  padding: 10px 15px;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.buttons {
  margin: 2px;
  width: 100%;
  height: 25%;
}

.form_buttons {
  margin: 2px;
  width: 50%;
  height: 100%;
}

#edit, #save {
  background-color: forestgreen;
}

#delete {
  background-color: firebrick;
}

#edit:hover, #save:hover {
  background-color: darkgreen;
}

#delete:hover {
  background-color: darkred;
}

#logout, #return, #manage {
  background-color: lightslategrey;
  text-decoration: none;
  text-align: center;
}

#logout:hover, #return:hover, #manage:hover {
  background-color: darkslategrey;
}
</style>