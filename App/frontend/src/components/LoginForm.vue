<script setup>
import { inject, ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const $cookies = inject('$cookies')

const username = ref('')
const password = ref('')
const show_password = ref(true)
const info = ref('')


// zablokowanie 'wklejania' tekstu do pola hasła i powtórzenia hasła
window.onload = () => {
  const password_input = document.getElementById('password')
  password_input.onpaste = e => e.preventDefault()
}

const loginUser = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/user/login',
        { params: { username: username.value, password: password.value } })
    $cookies.set('user', response.data)
    info.value = 'SUKCES!! Udało się zalogować.'
    await router.push('/profile')
  } catch (error) {
    const error_response = error.response.data
    if (typeof error_response['error'] === 'string') {
      info.value = error.response.data['error']
    } else {
      info.value = error.response.data['error'].join(' ')
    }
  }
}

if ($cookies.isKey('user')) {
  router.push('/profile')
}
</script>

<template>
  <div class="container">
    <div class="row">
      <form @submit.prevent="loginUser">
        <label for="username">Nazwa użytkownika</label>
        <input type="text" id="username" v-model="username"
               :style="{ backgroundColor: info.startsWith('BŁĄD') ? 'indianred' : '#ecf0f1' }">
        <label for="password">Hasło</label>
        <div class="password_part">
          <input v-if="show_password" id="password" type="password" v-model="password"
                 :style="{ backgroundColor: info.startsWith('BŁĄD') ? 'indianred' : '#ecf0f1' }">
          <input v-else id="password" type="text" v-model="password"
                 :style="{ backgroundColor: info.startsWith('BŁĄD') ? 'indianred' : '#ecf0f1' }">
          <button type="button" @click="show_password = !show_password">
            <i class="fas" :class="{ 'fa-eye-slash': show_password, 'fa-eye': !show_password }"></i>
          </button>
        </div>
        <button type="submit">Zaloguj się</button>
        <div class="info"
             :style="{
          color: info.startsWith('BŁĄD') ? 'darkred' : 'darkgreen', display: info.length === 0 ? 'none' : 'initial' }">
          {{ info }}
        </div>
      </form>
      <div class="links_column">
        <RouterLink to="/forgot_password" class="additional_links">Nie pamiętam hasła</RouterLink>
        <RouterLink to="/create_account" class="additional_links">Utwórz konto</RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  width: 80%;
  padding: 20px;
  height: 50%;
  margin: 0 auto;
  background-color: lightsteelblue;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.links_column {
  display: flex;
  flex-direction: column;
  width: 25%;
}

.row {
  display: flex;
  width: 100%;
  justify-content: space-evenly;
  align-items: center;
}

form {
  display: flex;
  flex-direction: column;
  width: 35%;
  height: 90%;
  padding: 20px;
  background-color: rgb(248, 249, 250);
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

label {
  margin-bottom: 8px;
  font-weight: bold;
  color: #2c3e50;
}

#password {
  width: 85%;
}

button[type="button"] {
  width: 15%;
}

.password_part {
  display: flex;
  flex-direction: row;
}

input[type="text"], input[type="password"], button[type="button"] {
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  font-size: 1rem;
  background-color: #ecf0f1;
  transition: border-color 0.3s;
}

button[type="submit"] {
  padding: 10px 15px;
  background-color: forestgreen;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

button[type="submit"]:hover {
  background-color: darkgreen;
}

p, li {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 8px;
}

p {
  color: #2c3e50;
}

.additional_links {
  margin-top: 20px;
  color: blue;
  font-size: 1.2rem;
  text-decoration: none;
  transition: color 0.3s ease;
  background-color: rgb(248, 249, 250);
  border-radius: 8px;
  padding: 20px;
  text-align: center;
}

.additional_links:hover {
  color: darkblue;
}

.info {
  padding-top: 20px;
  background-color: rgb(248, 249, 250);
  border-radius: 8px;
  color: darkred;
  font-size: 1rem;
}
</style>
