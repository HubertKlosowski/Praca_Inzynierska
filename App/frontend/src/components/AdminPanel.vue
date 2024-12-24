<script setup>
import axios from "axios";
import _ from "lodash";
import {onMounted, ref} from "vue";


const props = defineProps(['usertypes'])
const users_verify = ref([])

const after_create = defineModel('after_create')
const title = defineModel('title')
const subtitle = defineModel('subtitle')
const response_status = defineModel('response_status')


const verifyUser = async (user) => {
  try {
    const response = await axios.patch('http://localhost:8000/api/user/verify_user', {
      'username': user['username']
    })

    const index = _.indexOf(users_verify.value, user)
    users_verify.value[index]['is_verified'] = true
    localStorage.setItem('users_verify', JSON.stringify(users_verify.value))

    after_create.value = [user['username'], user['email']]
    title.value = response.data.success
    subtitle.value = 'Użytkownik został zweryfikowany.'
    response_status.value = response.status

  } catch (e) {
    if (typeof e.response === 'undefined') {
      after_create.value = ['BŁĄD!! Nie udało się połączyć z serwerem.']
      response_status.value = 500
      title.value = 'Problem z serwerem'
      subtitle.value = 'Proszę poczekać, serwer nie jest teraz dostępny.'
    } else {
      const error_response = e.response
      after_create.value = error_response.data.error
      response_status.value = error_response.status
      title.value = 'Problem z weryfikacją'
      subtitle.value = 'Próba weryfikacji użytkownika się nie powiodła. Proszę zapoznać się z błędem podanym poniżej i spróbować ponownie.'
    }
  }
}

const renewSubmission = async (user) => {
  try {
    const response = await axios.patch('http://localhost:8000/api/user/renew_submission/' + user['username'])

    const index = _.indexOf(users_verify.value, user)
    const submission_num = [10, 30, 100][user['usertype']]
    users_verify.value[index]['submission_num'] = submission_num
    localStorage.setItem('users_verify', JSON.stringify(users_verify.value))

    after_create.value = [user['username'], user['email'], submission_num]
    title.value = response.data.success
    subtitle.value = 'Liczba prób użytkownika została odnowiona.'
    response_status.value = response.status

  } catch (e) {
    if (typeof e.response === 'undefined') {
      after_create.value = ['BŁĄD!! Nie udało się połączyć z serwerem.']
      response_status.value = 500
      title.value = 'Problem z serwerem'
      subtitle.value = 'Proszę poczekać, serwer nie jest teraz dostępny.'
    } else {
      const error_response = e.response
      after_create.value = error_response.data.error
      response_status.value = error_response.status
      title.value = 'Problem z odnowieniem prób'
      subtitle.value = 'Próba odnowienia prób użytkownika się nie powiodła. Proszę zapoznać się z błędem podanym poniżej i spróbować ponownie.'
    }
  }
}

onMounted(() => {
  users_verify.value = JSON.parse(localStorage.getItem('users_verify'))
})
</script>

<template>
  <div class="users">
    <h3>Użytkownicy do zweryfikowania</h3>
    <div class="header-user-verify">
      <div class="field">Nazwa</div>
      <div class="field">Adres email</div>
      <div class="field">Zweryfikuj</div>
      <div class="field">Odnów próby</div>
    </div>
    <div class="u-verify">
      <div class="user-verify" v-for="u in users_verify" :key="u">
        <div class="field">
          <span>{{ u['username'] }}</span>
        </div>
        <div class="field">
          <span>{{ u['email'] }}</span>
        </div>
        <div class="field">
          <button type="button" class="verify" @click="verifyUser(u)" :style="{
            opacity: !u['is_verified'] ? '1' : '0.3',
            pointerEvents: !u['is_verified'] ? 'auto' : 'none'
          }">
            <font-awesome-icon :icon="['fas', 'check']" />
          </button>
        </div>
        <div class="field" style="border: none">
          <button type="button" class="renew" @click="renewSubmission(u)" :style="{
            opacity: u['submission_num'] !== [10, 30, 100][u['usertype']] ? '1' : '0.3',
            pointerEvents: u['submission_num'] !== [10, 30, 100][u['usertype']] ? 'auto' : 'none'
          }">
            <font-awesome-icon :icon="['fas', 'rotate']" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
svg {
  width: 100%;
  height: 100%;
}

.users {
  border-top: 2px solid black;
  height: 60%;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow-y: auto;
}

.u-verify {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
  overflow-y: scroll;
  scrollbar-gutter: stable both-edges;
}

.user-verify {
  width: 90%;
  min-height: 70%;
}

.header-user-verify {
  width: calc(90% - 24px);
  min-height: 20%;
}

.user-verify, .header-user-verify {
  margin: 1rem 0 1rem 0;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
  background-color: #f5f5f5;
  border-radius: 0.75rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.7);
}

.field {
  width: 40%;
  height: 80%;
  font-size: 1.5vw;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.user-verify > * {
  overflow-y: hidden;
  overflow-x: auto;
  border-right: 2px solid black;
}

.verify, .renew {
  width: 50%;
  height: 50%;
}

.verify, .renew {
  text-decoration: none;
  text-align: center;
  align-content: center;
  margin: 1rem;
  font-size: 1.25vw;
  transition: 0.4s ease;
  cursor: pointer;
  background-color: white;
  border-radius: 1rem;
}

.verify:hover, .renew:hover {
  color: white;
  border: 2px solid white;
  box-shadow: 0.5rem 0.5rem dodgerblue;
}

.verify:hover {
  background-color: darkgreen;
}

.renew:hover {
  background-color: darkgrey;
}

.verify {
  border: 2px solid green;
  color: green;
}

.renew {
  border: 2px solid black;
  color: black;
}

@media (max-width: 768px) {
  .buttons > * {
    width: 60%;
    height: 30%;
    font-size: 2vh;
  }

  .field {
    width: 80%;
    height: 20%;
    border: none;
  }

  .header-user-verify, .user-verify {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 50%;
  }

  h3, .field {
    font-size: 1.5vh;
  }
}
</style>