<script setup>
import {computed, ref} from "vue";

const name = ref('')
const surname = ref('')
const account_name = ref('')
const password = ref('')
const repeat_password = ref('')

const check_password_length = computed(() => password.value.length > 8)
const at_least_one_number = computed(() => new RegExp('[0-9]').test(password.value))
const at_least_one_capital = computed(() => new RegExp('[A-Z]').test(password.value))
const at_least_one_special = computed(() => new RegExp('[!@#$%^&*(),.?":{}|<>]').test(password.value))
const showPassword = ref(true)

const checkPassword = () => {
  // musi mieć conajmniej jedną cyfrę, dużą literę i znak specjalny
  return check_password_length && at_least_one_special && at_least_one_number && at_least_one_capital
}

const passwordsMatch = computed(() => {
  return repeat_password.value.length !== 0 && password.value.length !== 0 && repeat_password.value === password.value
})

// zablokowanie 'wklejania' tekstu do pola hasła i powtórzenia hasła
window.onload = () => {
  const password_input = document.getElementById('password')
  password_input.onpaste = e => e.preventDefault()
  const repeat_password_input = document.getElementById('repeat_password')
  repeat_password_input.onpaste = e => e.preventDefault()
}

const createAccount = () => {
  if (name.value.length === 0) {

  }
  return false
}
</script>

<template>
  <div class="container">
    <form @submit.prevent="createAccount">
      <label for="name">Imię</label>
      <input type="text" id="name" v-model="name">
      <label for="surname">Nazwisko</label>
      <input type="text" id="surname" v-model="surname">
      <label for="account_name">Nazwa konta</label>
      <input type="text" id="account_name" v-model="account_name">
      <label for="password">Hasło</label>
      <div class="password_part">
        <input v-if="showPassword" type="password" id="password" v-model="password">
        <input v-else type="text" id="password" v-model="password">
        <button type="button" @click="showPassword = !showPassword">
          <i class="fas" :class="{ 'fa-eye-slash': showPassword, 'fa-eye': !showPassword }"></i>
        </button>
      </div>
      <label for="repeat_password">Powtórz hasło</label>
      <input v-if="passwordsMatch === true" style="background-color: lightgreen" type="password" id="repeat_password" v-model="repeat_password">
      <input v-else style="background-color: indianred" type="password" id="repeat_password" v-model="repeat_password">
      <button type="submit">Załóż konto</button>
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
  flex-direction: row;
  justify-content: space-evenly;
}

.password_requirements {
  width: 45%;
  background-color: #f8f9fa;
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
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

button[type="submit"]:hover {
  background-color: #2980b9;
}
</style>