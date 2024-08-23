<script setup>
import {computed, ref} from 'vue'

const name = ref('')
const password = ref('')
const check_length = computed(() => password.value.length > 8)
const at_least_one_number = computed(() => new RegExp('[0-9]').test(password.value))
const at_least_one_capital = computed(() => new RegExp('[A-Z]').test(password.value))
const at_least_one_special = computed(() => new RegExp('[!@#$%^&*(),.?":{}|<>]').test(password.value))


const checkPassword = () => {
  // musi mieć conajmniej jedną cyfrę, dużą literę i znak specjalny
  return check_length && at_least_one_special && at_least_one_number && at_least_one_capital
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
        <input type="text" id="password" v-model="password">
        <button type="submit">Zaloguj się</button>

      </form>
      <div class="password_requirements">
        <p>Hasło musi mieć conajmniej:</p>
        <ol type="I">
          <li :style="{ color: check_length ? 'darkgreen' : 'darkred' }">8 znaków</li>
          <li :style="{ color: at_least_one_number ? 'darkgreen' : 'darkred' }">1 cyfrę</li>
          <li :style="{ color: at_least_one_capital ? 'darkgreen' : 'darkred' }">1 wielką literę</li>
          <li :style="{ color: at_least_one_special ? 'darkgreen' : 'darkred' }">1 znak specjalny</li>
        </ol>
      </div>
    </div>
    <RouterLink to="/forgot_passwd" class="forgot_password">Nie pamiętam hasła</RouterLink>
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
}

.row {
  display: flex;
  width: 100%;
  justify-content: space-between;
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

input[type="text"] {
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
