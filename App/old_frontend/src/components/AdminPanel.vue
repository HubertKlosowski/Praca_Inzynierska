<script setup>
import { reactive, onMounted, inject, ref, watchEffect } from 'vue'
import axios from 'axios'

const users = reactive([])
const $cookies = inject('$cookies')
const user_types = ['Normal', 'Pro', 'Admin']
const info = ref('')

onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/user/get_users')
    let data = response.data
    data = data.filter(user => user.username !== $cookies.get('user')['username'])
    users.push(...data)
  } catch (error) {
    console.log(error)
  }
})

const deleteUser = async (user) => {
  try {
    const to_delete = await axios.delete('http://localhost:8000/api/user/delete_user/' + user['username'])
    info.value = to_delete.data['success']
    document.getElementById(user.id).remove()
  } catch (error) {
    const error_response = error.response.data
    if (typeof error_response['error'] === 'string') {
      info.value = error_response['error']
    } else if (typeof error_response['error'] === 'undefined') {
      info.value = 'BŁĄD!! Nie udało się połączyć z serwerem.'
    } else {
      info.value = error_response['error'].join(' ')
    }
  }
}

const renewSubmissions = async (user) => {
  try {
    const to_update = await axios.patch('http://localhost:8000/api/user/renew_submission/' + user['username'])
    info.value = to_update.data['success']
    const element = document.getElementById(user.id).childNodes[3]
    element.textContent = to_update.data['user'].submission_num
  } catch (error) {
    const error_response = error.response.data
    if (typeof error_response['error'] === 'string') {
      info.value = error_response['error']
    } else if (typeof error_response['error'] === 'undefined') {
      info.value = 'BŁĄD!! Nie udało się połączyć z serwerem.'
    } else {
      info.value = error_response['error'].join(' ')
    }
  }
}

const verifyUser = async (user) => {
  try {
    const to_verify = await axios.patch('http://localhost:8000/api/user/verify_user/' + user['username'])
    info.value = to_verify.data['success']
  } catch (error) {
    const error_response = error.response.data
    if (typeof error_response['error'] === 'string') {
      info.value = error_response['error']
    } else if (typeof error_response['error'] === 'undefined') {
      info.value = 'BŁĄD!! Nie udało się połączyć z serwerem.'
    } else {
      info.value = error_response['error'].join(' ')
    }
  }
}
</script>

<template>
  <div class="container">
    <div class="row title">
      <div>Nazwa użytkownika</div>
      <div>Email</div>
      <div>Typ konta</div>
      <div>Liczba prób</div>
      <div>Usuń</div>
      <div>Odnów próby</div>
      <div>Zweryfikuj</div>
    </div>
    <div class="users">
      <div class="row center" v-for="user in users" :key="user.id" :id="user.id">
        <div>{{ user.username }}</div>
        <div>{{ user.email }}</div>
        <div>{{ user_types[user.usertype] }}</div>
        <div>{{ user.submission_num }}</div>
        <button type="button" class="delete" @click="deleteUser(user)">
          &#10006;
        </button>
        <button type="button" class="renew" @click="renewSubmissions(user)">
          &#8635;
        </button>
        <button type="button" class="verify" @click="verifyUser(user)">
          &#10004;
        </button>
      </div>
    </div>
    <div class="rest">
      <div
          class="error"
          :style="{ color: info.startsWith('BŁĄD') ? 'darkred' : 'darkgreen',
          display: info.length === 0 ? 'none' : 'initial' }">
        {{ info }}
      </div>
      <button type="button" id="return" class="buttons" @click="$emit('goBack', false)">Wróć</button>
    </div>
  </div>
</template>

<style scoped>
.users {
  display: flex;
  flex-direction: column;
  width: 90%;
  height: 60%;
  max-height: 60vh;
  overflow-y: auto;
}

.title {
  width: 90%;
}

.rest {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  width: 100%;
  height: 20%;
  align-items: center;
}

.error {
  width: 70%;
  height: 30%;
  padding: 20px;
  background-color: rgb(248, 249, 250);
  border-radius: 8px;
  color: darkred;
  font-size: 1.2rem;
}

#return {
  width: 20%;
  height: 30%;
  background-color: lightslategrey;
  text-decoration: none;
  text-align: center;
  font-size: 1.2rem;
  border-radius: 8px;
  padding: 10px 15px;
  color: white;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
}

#return:hover {
  background-color: darkslategrey;
}

.row {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  margin: 10px;
  background-color: rgb(248, 249, 250);
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  color: #2c3e50;
}

div {
  text-align: center;
}

.row > :first-child {
  width: 30%;
}

.row > :nth-child(2) {
  width: 20%;
}

.row > :nth-child(n + 3) {
  width: 7%;
}

button[type="button"] {
  font-size: 1.2rem;
  color: #f1f1f1;
  border-radius: 8px;
  border: none;
  cursor: pointer;
}

.delete {
  background-color: firebrick;
}

.renew {
  background-color: forestgreen;
}

.delete:hover {
  background-color: darkred;
}

.renew:hover {
  background-color: darkgreen;
}

.verify {
  background-color: orange;
}

.verify:hover {
  background-color: darkorange;
}
</style>