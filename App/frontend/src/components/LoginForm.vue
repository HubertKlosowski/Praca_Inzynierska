<script setup>
import {computed, ref} from "vue"

const name = ref('')
const password = ref('')
const check_password_length = computed(() => password.value.length > 8)
const at_least_one_number = computed(() => new RegExp('[0-9]').test(password.value))
const at_least_one_capital = computed(() => new RegExp('[A-Z]').test(password.value))
const at_least_one_special = computed(() => new RegExp('[!@#$%^&*(),.?":{}|<>]').test(password.value))
const showPassword = ref(true)

const checkPassword = () => {
  // musi mieć conajmniej jedną cyfrę, dużą literę i znak specjalny
  return check_password_length && at_least_one_special && at_least_one_number && at_least_one_capital
}

// zablokowanie 'wklejania' tekstu do pola hasła i powtórzenia hasła
window.onload = () => {
  const password_input = document.getElementById('password')
  password_input.onpaste = e => e.preventDefault()
}

const loginUser = () => {
  if (checkPassword(password.value)) {
    console.log(name, password)
  } else {
    console.log('Cos chyba nie dziala')
  }
}
</script>

<template>
  <div class="container">
    <div class="row">
      <form @submit.prevent="loginUser">
        <label for="username">Nazwa użytkownika</label>
        <input type="text" id="username" v-model="name">
        <label for="password">Hasło</label>
        <div class="password_part">
          <input v-if="showPassword" id="password" type="password" v-model="password">
          <input v-else id="password" type="text" v-model="password">
          <button type="button" @click="showPassword = !showPassword">
            <i class="fas" :class="{ 'fa-eye-slash': showPassword, 'fa-eye': !showPassword }"></i>
          </button>
        </div>
        <button type="submit">Zaloguj się</button>
      </form>
      <div class="password_requirements">
        <p>Hasło musi mieć conajmniej:</p>
        <ol type="1">
          <li :style="{ color: check_password_length ? 'darkgreen' : 'darkred' }">osiem znaków</li>
          <li :style="{ color: at_least_one_number ? 'darkgreen' : 'darkred' }">jedną cyfrę</li>
          <li :style="{ color: at_least_one_capital ? 'darkgreen' : 'darkred' }">jedną wielką literę</li>
          <li :style="{ color: at_least_one_special ? 'darkgreen' : 'darkred' }">jeden znak specjalny</li>
        </ol>
      </div>
    </div>
    <RouterLink to="/forgot_passwd" class="forgot_password">Nie pamiętam hasła</RouterLink>
    <RouterLink to="/create_account" class="forgot_password">Utwórz konto</RouterLink>
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

.row {
  display: flex;
  width: 100%;
  justify-content: space-evenly;
  align-items: center;
}

form {
  display: flex;
  flex-direction: column;
  width: 45%;
  height: 90%;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.password_requirements {
  width: 45%;
  background-color: #f8f9fa;
  height: 90%;
  padding: 20px;
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

input[type="text"]:focus {
  border-color: #3498db;
  outline: none;
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

.forgot_password {
  margin-top: 20px;
  color: blue;
  font-size: 1rem;
  text-decoration: none;
  padding: 5px;
  transition: color 0.3s ease;
}

.forgot_password:hover {
  color: darkblue;
}
</style>
