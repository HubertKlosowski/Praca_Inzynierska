<script setup>
import { inject, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from "axios";

const router = useRouter()

const usertypes = ['Normal', 'Pro', 'Admin']

const editUserData = ref(false)
const name = ref('')
const username = ref('')
const usertype = ref(0)
const email = ref('')

const $cookies = inject('$cookies')

const saveChanges = () => {
  editUserData.value = false
}

const deleteUser = async () => {
  try {
    const to_del = await axios.delete('http://localhost:8000/api/user/delete_user/' + $cookies.get('user')['username'])
    console.log(to_del)
    $cookies.remove('user')
    await router.push('/')
  } catch (error) {
    console.log(error)
  }
}

const logout = () => {
  $cookies.remove('user')
  router.push('/')
}
</script>

<template>
  <div class="container">
    <div class="row main_row">
      <div class="image">
        <img src="@/assets/user.png" alt="Ikonka">
        <div class="create_at">
          Utworzony: {{ $cookies.get('user')['created_at'].slice(0, 10) }}
        </div>
        <button @click="editUserData = !editUserData" id="edit" v-show="!editUserData">Edytuj</button>
        <button @click="deleteUser" id="delete" v-show="!editUserData">Usuń</button>
        <button @click="logout" id="logout">Wyloguj</button>
      </div>
      <div class="column" v-show="!editUserData">
        <div class="row user_row">
          <div class="name">
            Imię: {{ $cookies.get('user')['name'] }}
          </div>
          <div class="username">
            Nazwa użytkownika: {{ $cookies.get('user')['username'] }}
          </div>
        </div>
        <div class="row user_row">
          <div class="email">
            Email: {{ $cookies.get('user')['email'] }}
          </div>
          <div class="usertype">
            Typ konta: {{ usertypes[$cookies.get('user')['usertype']] }}
          </div>
        </div>
      </div>
      <div class="form">
        <form @submit.prevent="saveChanges" v-show="editUserData">
          <div class="form_row">
            <label for="name">Imię:</label>
            <input type="text" v-model="name" id="name">
            <label for="username">Nazwa użytkownika</label>
            <input type="text" v-model="username" id="username">
          </div>
          <div class="form_row">
            <label for="email">Email:</label>
            <input type="text" v-model="email" id="email">
            <label for="usertype">Typ konta</label>
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
          </div>
          <div class="form_row">
            <button type="submit" id="save">Zapisz</button>
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
</template>

<style scoped>
.container {
  width: 80%;
  padding: 20px;
  height: 80%;
  margin: 0 auto;
  background-color: lightsteelblue;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-evenly;
}

.row {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  color: #2c3e50;
  padding: 10px;
}

.main_row {
  width: 100%;
  height: 30%;
}

.user_row {
  justify-content: space-around;
}

.column {
  display: flex;
  flex-direction: column;
}

.column, .form {
  width: 75%;
  height: 25%;
}

.form {
  justify-content: end;
}

form {
  width: 75%;
  height: 25%;
  display: grid;
  grid-template-columns: 1fr 2fr;
  grid-gap: 15px;
}

.form_row {
  display: contents;
}

.submission {
  width: 25%;
  height: 100%;
  background-color: rgb(248, 249, 250);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

img {
  width: 100%;
  height: 100%;
}

.image {
  width: 15%;
  height: auto;
  display: flex;
  flex-direction: column;
}

.create_at {
  text-align: center;
}

.name, .username, .usertype, .email {
  width: 25%;
  height: 25%;
}

.checkbox_row {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
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

#logout {
  background-color: lightslategrey;
  text-decoration: none;
  text-align: center;
}

#logout:hover {
  background-color: darkslategrey;
}
</style>