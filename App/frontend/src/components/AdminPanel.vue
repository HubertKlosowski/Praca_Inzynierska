<script setup>
import axios from "axios";
import _ from "lodash";
import {reactive, ref} from "vue";


const users_verify = ref(JSON.parse(localStorage.getItem('users_verify')))

const after_create = defineModel('after_create')
const title = defineModel('title')
const subtitle = defineModel('subtitle')
const response_status = defineModel('response_status', {required: true})
const token = reactive(JSON.parse(localStorage.getItem('token')))


const verifyUser = async (user) => {
  let status
  try {
    const response = await axios.patch('http://localhost:8000/api/user/verify_user',
        {'username': user['username']},
        {headers: {'Authorization' : `Bearer ${token['access']}`}}
    )

    const index = _.indexOf(users_verify.value, user)
    users_verify.value[index]['is_verified'] = true
    localStorage.setItem('users_verify', JSON.stringify(users_verify.value))

    after_create.value = [
      ['Nazwa użytkownika', user['username']],
      ['Adres email', user['email']]
    ]
    title.value = response.data.success
    subtitle.value = 'Użytkownik został zweryfikowany.'
    status = response.status

  } catch (e) {
    if (typeof e.response === 'undefined') {
      after_create.value = ['Nie udało się połączyć z serwerem.']
      status = 500
      title.value = 'Problem z serwerem'
      subtitle.value = 'Proszę poczekać, serwer nie jest teraz dostępny.'
    } else {
      const error_response = e.response
      status = error_response.status
      after_create.value = error_response.data.error
      subtitle.value = 'Weryfikacja użytkownika ' + user['username'] + ' się nie powiodła. Proszę zapoznać się z błędem podanym poniżej i spróbować ponownie.'

      if (status === 429) {
        title.value = 'Przekroczony limit weryfikacji innych użytkowników'
      } else if (status === 403) {
        title.value = 'Problem z weryfikacją użytkownika'
        if (error_response.data.code === 'access_token_failed') {  // jeśli access_token wygaśnie
          await refreshAccessToken(['Twoje dane wygasły, ale zostały odświeżone.', 'Teraz możesz zweryfikować konto użytkownika ' + user['username'] + '.'])
        }
      } else {
        title.value = 'Problem z danymi'
      }
    }
  }
  response_status.value = status
}

const renewSubmission = async (user) => {
  let status
  try {
    const response = await axios.patch('http://localhost:8000/api/user/renew_submission',
        {'username': user['username']},
        {headers: {'Authorization' : `Bearer ${token['access']}`}}
    )

    const index = _.indexOf(users_verify.value, user)
    const submission_num = [10, 30, 100][user['usertype']]
    users_verify.value[index]['submission_num'] = submission_num
    localStorage.setItem('users_verify', JSON.stringify(users_verify.value))

    after_create.value = [
      ['Nazwa użytkownika', user['username']],
      ['Adres email', user['email']],
      ['Dzienne próby', submission_num]
    ]
    title.value = response.data.success
    subtitle.value = 'Liczba prób użytkownika została odnowiona.'
    status = response.status

  } catch (e) {
    if (typeof e.response === 'undefined') {
      after_create.value = ['Nie udało się połączyć z serwerem.']
      status = 500
      title.value = 'Problem z serwerem'
      subtitle.value = 'Proszę poczekać, serwer nie jest teraz dostępny.'
    } else {
      const error_response = e.response
      after_create.value = error_response.data.error
      status = error_response.status
      subtitle.value = 'Odnowienie prób użytkownika ' + user['username'] + ' się nie powiodło. Proszę zapoznać się z błędem podanym poniżej i spróbować ponownie.'

      if (status === 429) {
        title.value = 'Przekroczony limit odnowień prób innych użytkowników'
      } else if (status === 403) {
        title.value = 'Problem z weryfikacją użytkownika'
        if (error_response.data.code === 'access_token_failed') {  // jeśli access_token wygaśnie
          await refreshAccessToken(['Twoje dane wygasły, ale zostały odświeżone.', 'Teraz możesz odnowić próby dla użytkownika ' + user['username'] + '.'])
        }
      } else {
        title.value = 'Problem z danymi'
      }
    }
  }
  response_status.value = status
}

const refreshAccessToken = async (after_create_success) => {
  try {
    const response = await axios.post('http://localhost:8000/api/token/refresh', {
      'refresh': token.refresh
    })

    token.access = response.data['access']
    localStorage.setItem('token', JSON.stringify(token))

    after_create.value = after_create_success
    response_status.value = 199  // błąd nie spowodowany działaniem użytkownika

  } catch (e) {
    const error_response = e.response
    response_status.value = error_response.status
    after_create.value = error_response.data.error
    title.value = 'Problem z danymi logowania'  // jeśli refresh_token wygaśnie
  }
}
</script>

<template>
  <div class="users">
    <h3>Użytkownicy do zweryfikowania</h3>
    <div class="header-user-verify">
      <div class="field">Nazwa użytkownika</div>
      <div class="field">Adres email</div>
      <div class="field">Zweryfikuj</div>
      <div class="field">Odnów próby</div>
    </div>
    <div class="u-verify">
      <div class="user-verify" v-for="u in users_verify" :key="u" v-if="!_.isEmpty(users_verify)">
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
      <div class="user-verify" v-else>
        Brak użytkowników
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
  font-size: 1.5vw;
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

@media (max-width: 700px) {
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

  h3, .field, .user-verify {
    font-size: 1.5vh;
  }
}
</style>