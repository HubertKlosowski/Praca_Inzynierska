<script setup>
import { computed, ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import SetPassword from '@/components/SetPassword.vue'

const router = useRouter()

const name = ref('')
const email = ref('')
const username = ref('')
const password = ref('')
const repeat_password = ref('')
const usertype = ref(0)
const show_password = ref(true)

const info = ref('')
const check_password_length = computed(() => password.value.length > 8)
const at_least_one_number = computed(() => new RegExp('[0-9]').test(password.value))
const at_least_one_capital = computed(() => new RegExp('[A-Z]').test(password.value))
const at_least_one_special = computed(() => new RegExp('[!@#$%^&*(),.?":{}|<>]').test(password.value.trim()))
const check_email = computed(() => new RegExp('^[a-zA-Z0-9]+@[a-zA-Z0-9]+\\.[a-zA-Z]{2,}$').test(email.value.trim()))
const passwords_match = computed(() => {
  return repeat_password.value === password.value
})

// zablokowanie 'wklejania' tekstu do pola hasła i powtórzenia hasła
window.onload = () => {
  const password_input = document.getElementById('password')
  password_input.onpaste = e => e.preventDefault()
  const repeat_password_input = document.getElementById('repeat_password')
  repeat_password_input.onpaste = e => e.preventDefault()
}

const resetInputs = () => {
  name.value = ''
  email.value = ''
  username.value = ''
  password.value = ''
  repeat_password.value = ''
  usertype.value = 0
  show_password.value = true
}

const isDataValid = async () => {
  if (!passwords_match.value) {
    return 'BŁĄD!! Wpisane hasła nie pasują do siebie.'
  } else if (!check_email.value) {
    return 'BŁĄD!! Email nie spełnia wymagań.'
  }
  return 'SUKCES!! Email i hasła spełniają wymagania.'
}

const createAccount = async () => {
  const sub_num = [10, 30, 100][+usertype.value] || 10
  info.value = await isDataValid()
  if (info.value.startsWith('SUKCES!!')) {
    try {
      const response = await axios.post('http://localhost:8000/api/user/create_user', {
        name: name.value,
        email: email.value,
        username: username.value,
        usertype: +usertype.value,
        password: password.value,
        submission_num: sub_num
      })
      info.value = response.data['success']

      resetInputs()
      await new Promise(resolve => setTimeout(resolve, 1000))
      await router.push('/login')
    } catch (error) {
      const error_response = error.response.data
      if (typeof error_response['error'] === 'string') {
        info.value = error_response['error']
      } else {
        info.value = error_response['error'].join(' ')
      }
    }
  }
}
</script>

<template>
  <div class="container">
    <form @submit.prevent="createAccount">
      <label for="name">Imię i Nazwisko</label>
      <input type="text" id="name" v-model="name">

      <label for="email">Email</label>
      <input type="text" id="email" v-model="email">

      <label for="username">Nazwa konta</label>
      <input type="text" id="username" v-model="username">

      <label>Typ konta</label>

      <div class="checkbox_column">
        <div class="checkbox_row">
          <label for="normal">Normal</label>
          <label for="pro">Pro</label>
          <label for="admin">Admin</label>
        </div>
        <div class="checkbox_row">
          <input type="radio" id="normal" value="0" v-model="usertype">
          <input type="radio" id="pro" value="1" v-model="usertype">
          <input type="radio" id="admin" value="2" v-model="usertype">
        </div>
      </div>

      <SetPassword @set-password="(passwd) => password = passwd"></SetPassword>

      <label for="repeat_password">Powtórz hasło</label>
      <input :style="{ backgroundColor: passwords_match ? '#ecf0f1' : 'indianred' }" type="password" id="repeat_password" v-model="repeat_password">

      <div class="buttons_row">
        <button type="submit">Załóż konto</button>
        <button type="reset" @click="resetInputs">Resetuj</button>
      </div>
    </form>

    <div class="not_form_column">
      <div class="password_requirements">
        <p>Hasło musi mieć conajmniej:</p>
        <ol type="1">
          <li :style="{ color: check_password_length ? 'darkgreen' : 'darkred' }">osiem znaków</li>
          <li :style="{ color: at_least_one_number ? 'darkgreen' : 'darkred' }">jedną cyfrę</li>
          <li :style="{ color: at_least_one_capital ? 'darkgreen' : 'darkred' }">jedną wielką literę</li>
          <li :style="{ color: at_least_one_special ? 'darkgreen' : 'darkred' }">jeden znak specjalny</li>
        </ol>
      </div>
      <div
          class="info"
          :style="{
        color: info.startsWith('BŁĄD') ? 'darkred' : 'darkgreen',
        display: info.length === 0 ? 'none' : 'initial' }">
        {{ info }}
      </div>
      <div class="go_back_to_login">
        <RouterLink to="/login" class="additional_links">Wróć do logowania</RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  width: 80%;
  padding: 20px;
  height: 70%;
  margin: 0 auto;
  background-color: lightsteelblue;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
}

.not_form_column {
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
  width: 35%;
}

.checkbox_row {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}

input[type="radio"] {
  width: 1.2rem;
  height: 1.2rem;
  transform: translateY(-0.15em);
}

.password_requirements {
  background-color: rgb(248, 249, 250);
  height: 50%;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

p {
  color: #2c3e50;
}

p, li {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 8px;
}

button[type="reset"] {
  padding: 10px 15px;
  background-color: lightslategrey;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

button[type="reset"]:hover {
  background-color: darkslategrey;
}

.buttons_row {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
}

.buttons_row > * {
  width: 35%;
}

form {
  display: flex;
  flex-direction: column;
  width: 55%;
  padding: 20px;
  background-color: rgb(248, 249, 250);
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

label {
  margin-bottom: 4px;
  font-weight: bold;
  color: #2c3e50;
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

.additional_links {
  margin-top: 20px;
  color: blue;
  font-size: 1.2rem;
  text-decoration: none;
  padding: 20px;
  transition: color 0.3s ease;
  background-color: rgb(248, 249, 250);
  border-radius: 8px;
  text-align: center;
}

.additional_links:hover {
  color: darkblue;
}

.info {
  padding: 20px;
  background-color: rgb(248, 249, 250);
  border-radius: 8px;
  color: darkred;
  font-size: 1.2rem;
}
</style>