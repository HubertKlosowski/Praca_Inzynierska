<script setup>
import {inject, onMounted, ref} from "vue";
import polish from "@/assets/polski.png";
import english from "@/assets/angielski.png";
import {useRouter} from "vue-router";
import axios from "axios";
import ResponseOutput from "@/components/ResponseOutput.vue";
import _ from "lodash";
import UpdateAccount from "@/components/UpdateAccount.vue";

const router = useRouter()
const $cookies = inject('$cookies')

const user = ref(JSON.parse(localStorage.getItem('user')))
const usertypes = ['Normal', 'Pro', 'Administrator']

const show_update_form = ref(false)
const choose_polish = ref(false)
const choose_english = ref(false)
const history_submissions = ref(JSON.parse(localStorage.getItem('history_submissions')))
const users_verify = ref([])
const models = ref(['roberta-base', 'bert-base'])

const after_create = ref({})
const title = ref('')
const subtitle = ref('')
const response_status = ref(0)

const logoutUser = async () => {
  localStorage.clear()
  $cookies.remove('made_submission')
  await router.push('/')
}

const deleteUser = async () => {
  try {
    const response = await axios.delete('http://localhost:8000/api/user/delete_user/' + user.value['username'])

    after_create.value = [user.value['username'], user.value['email']]
    title.value = response.data.success
    subtitle.value = 'Użytkownik poprawnie usunięty.'
    response_status.value = response.status
    await logoutUser()

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
      title.value = 'Problem z usunięciem konta'
      subtitle.value = 'Próba usunięcia konta się nie powiodła. Proszę zapoznać się z błędem podanym poniżej i spróbować ponownie.'
    }
  }
}

const verifyUser = async (user) => {
  try {
    const response = await axios.patch('http://localhost:8000/api/user/verify_user/' + user['username'])

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

const setPolishModel = () => {
  choose_polish.value = !choose_polish.value
  models.value[0] = choose_polish.value ? 'roberta-large' : 'roberta-base'
  localStorage.setItem('choosen_models', JSON.stringify(models.value))
}

const setEnglishModel = () => {
  choose_english.value = !choose_english.value
  models.value[1] = choose_english.value ? 'bert-large' : 'bert-base'
  localStorage.setItem('choosen_models', JSON.stringify(models.value))
}

const showDetails = async (submission) => {
  try {
    const response = await axios.get('http://localhost:8000/api/submission/get_submission/' + submission['id'])

    localStorage.setItem('depressed', JSON.stringify(response.data['depressed']))
    localStorage.setItem('text', JSON.stringify(response.data['text']))
    localStorage.setItem('choosen_submission', JSON.stringify(submission))

    await router.push('/predict')

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
      title.value = 'Problem z odczytaniem rezultatów'
      subtitle.value = 'Podczas szukania rezultatów wystąpił błąd. Proszę zapoznać się z błędem podanym poniżej i spróbować ponownie.'
    }
  }
}

onMounted(() => {
  if (user.value['usertype'] === 2) {
    users_verify.value = JSON.parse(localStorage.getItem('users_verify'))
  } else {
    users_verify.value = []
  }

  if (JSON.parse(localStorage.getItem('choosen_models')) === null) {
    localStorage.setItem('choosen_models', JSON.stringify(models.value))
  } else {
    models.value = JSON.parse(localStorage.getItem('choosen_models'))
    choose_polish.value = models.value[0] !== 'roberta-base'
    choose_english.value = models.value[1] !== 'bert-base'
  }
})
</script>

<template>

  <ResponseOutput
      v-model:response_status="response_status"
      v-model:after_create="after_create"
      v-if="response_status >= 200"
      :title="title"
      :subtitle="subtitle"
  ></ResponseOutput>

  <UpdateAccount
      v-if="show_update_form"
  ></UpdateAccount>

  <div class="left-part" :style="{
    opacity: response_status < 200 ? '1' : '0.3',
    pointerEvents: response_status < 200 ? 'auto' : 'none'
  }" v-else>
    <div class="header">
      <h3>Witaj {{ user['username'] }}!</h3>
      <div class="info">{{ user['name'] }}</div>
      <div class="info">{{ user['email'] }}</div>
      <div class="info">{{ usertypes[user['usertype']] }}</div>
      <div class="info">{{ user['submission_num'] }}</div>
      <button type="button" class="logout" @click="logoutUser">Wyloguj się</button>
    </div>
    <div class="model-config">
      <h3>Konfiguracja modelu</h3>
      <div class="models">
        <h3>LARGE</h3>
        <div class="t-buttons">
          <div
              class="toggle-button"
              :style="{ justifyContent: choose_polish ? 'start' : 'end' }"
              @click="setPolishModel">
            <div class="circle" :style="{
              backgroundImage: `url(${polish})`,
              backgroundRepeat: 'no-repeat',
              backgroundSize: 'cover',
              backgroundPosition: 'center'
            }"></div>
          </div>
          <div
              class="toggle-button"
              :style="{ justifyContent: choose_english ? 'start' : 'end' }"
              @click="setEnglishModel">
            <div class="circle" :style="{
              backgroundImage: `url(${english})`,
              backgroundRepeat: 'no-repeat',
              backgroundSize: 'cover',
              backgroundPosition: 'center'
            }"></div>
          </div>
        </div>
        <h3>BASE</h3>
      </div>
    </div>
    <div class="history">
      <h3>Historia predykcji</h3>
      <div class="header-user-verify">
        <div class="field">Numer</div>
        <div class="field">Nazwa</div>
        <div class="field">Szczegóły</div>
      </div>
      <div class="h-submissions">
        <div class="history-submission" v-for="(item, i) in history_submissions" :key="item">
          <div class="field" style="width: 10%">{{ i + 1 }}</div>
          <div class="field" v-if="item.name !== null">{{ item.name }}</div>
          <div class="field" v-else>Brak nazwy</div>
          <div class="field">
            <button type="button" class="details" @click="showDetails(item)">Pokaż szczegóły</button>
          </div>
        </div>
      </div>
    </div>
    <div class="users" v-if="user['usertype'] === 2">
      <h3>Użytkownicy do zweryfikowania</h3>
      <div class="header-user-verify">
        <div class="field">Nazwa</div>
        <div class="field">Adres email</div>
        <div class="field">Typ konta</div>
        <div class="field">Liczba prób</div>
        <div class="field">Zweryfikuj</div>
        <div class="field">Odnów próby</div>
      </div>
      <div class="u-verify">
        <div class="user-verify" v-for="user in users_verify" :key="user">
          <div class="field">
            <span>{{ user['username'] }}</span>
          </div>
          <div class="field">
            <span>{{ user['email'] }}</span>
          </div>
          <div class="field">
            <span>{{ usertypes[user['usertype']] }}</span>
          </div>
          <div class="field">
            <span>{{ user['submission_num'] }}</span>
          </div>
          <div class="field">
            <button type="button" class="verify" @click="verifyUser(user)" :style="{
              opacity: !user['is_verified'] ? '1' : '0.3',
              pointerEvents: !user['is_verified'] ? 'auto' : 'none'
            }">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">
                <path d="M438.6 105.4c12.5 12.5 12.5 32.8 0 45.3l-256 256c-12.5 12.5-32.8 12.5-45.3 0l-128-128c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L160 338.7 393.4 105.4c12.5-12.5 32.8-12.5 45.3 0z"/>
              </svg>
            </button>
            <button type="button" class="renew" @click="renewSubmission(user)" :style="{
              opacity: user['submission_num'] !== [10, 30, 100][user['usertype']] ? '1' : '0.3',
              pointerEvents: user['submission_num'] !== [10, 30, 100][user['usertype']] ? 'auto' : 'none'
            }">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                <path d="M105.1 202.6c7.7-21.8 20.2-42.3 37.8-59.8c62.5-62.5 163.8-62.5 226.3 0L386.3 160 352 160c-17.7 0-32 14.3-32 32s14.3 32 32 32l111.5 0c0 0 0 0 0 0l.4 0c17.7 0 32-14.3 32-32l0-112c0-17.7-14.3-32-32-32s-32 14.3-32 32l0 35.2L414.4 97.6c-87.5-87.5-229.3-87.5-316.8 0C73.2 122 55.6 150.7 44.8 181.4c-5.9 16.7 2.9 34.9 19.5 40.8s34.9-2.9 40.8-19.5zM39 289.3c-5 1.5-9.8 4.2-13.7 8.2c-4 4-6.7 8.8-8.1 14c-.3 1.2-.6 2.5-.8 3.8c-.3 1.7-.4 3.4-.4 5.1L16 432c0 17.7 14.3 32 32 32s32-14.3 32-32l0-35.1 17.6 17.5c0 0 0 0 0 0c87.5 87.4 229.3 87.4 316.7 0c24.4-24.4 42.1-53.1 52.9-83.8c5.9-16.7-2.9-34.9-19.5-40.8s-34.9 2.9-40.8 19.5c-7.7 21.8-20.2 42.3-37.8 59.8c-62.5 62.5-163.8 62.5-226.3 0l-.1-.1L125.6 352l34.4 0c17.7 0 32-14.3 32-32s-14.3-32-32-32L48.4 288c-1.6 0-3.2 .1-4.8 .3s-3.1 .5-4.6 1z"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="buttons">
      <button type="button" @click="show_update_form = true" class="update">Zmień dane</button>
      <button type="button" @click="deleteUser" class="delete">Usuń konto</button>
      <RouterLink to="/" class="router-link">Wróć do strony głównej</RouterLink>
    </div>
  </div>
</template>

<style scoped>
svg {
  width: 100%;
  height: 100%;
}

.history, .users {
  border-top: 2px solid black;
  height: 60%;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow-y: auto;
}

.h-submissions, .u-verify {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
  overflow-y: auto;
}

.history-submission, .user-verify, .header-user-verify {
  width: 90%;
  min-height: 50%;
  margin: 1rem 0 1rem 0;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
  background-color: #f5f5f5;
  border-radius: 0.75rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.7);
}

.header-user-verify {
  width: 100%;
  min-height: 20%;
}

.field {
  width: 40%;
  height: 80%;
  font-size: 1.5vw;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.field button {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.model-config {
  border-top: 2px solid black;
  height: 40%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}

.models {
  width: 50%;
  height: 90%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}

.t-buttons {
  width: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.toggle-button {
  width: 80%;
  margin: 0.5rem;
  background-color: gray;
  border-radius: 4vw;
  display: flex;
  flex-direction: row;
  align-items: center;
}

.circle {
  width: 4vw;
  height: 4vw;
  border-radius: 50%;
  border: 2px solid black;
  transition: transform 0.3s ease;
}

.logout {
  width: 10%;
  height: 60%;
}

.details {
  width: 80%;
  height: 60%;
}

.update, .delete {
  width: 30%;
  height: 60%;
}

.verify, .renew {
  width: 50%;
  height: 50%;
}

.update, .delete, .logout, .details, .verify, .renew {
  text-decoration: none;
  text-align: center;
  align-content: center;
  margin: 1rem;
  font-size: 1.35vw;
  transition: 0.4s ease;
  cursor: pointer;
  background-color: white;
  border-radius: 1rem;
}

.update:hover, .delete:hover, .logout:hover, .details:hover, .verify:hover, .renew:hover {
  color: white;
  border: 2px solid white;
  box-shadow: 1rem 1rem dodgerblue;
}

.details:hover, .logout:hover {
  background-color: black;
}

.update:hover, .verify:hover {
  background-color: darkgreen;
}

.delete:hover {
  background-color: darkred;
}

.renew:hover {
  background-color: darkgrey;
}

.update, .verify {
  border: 2px solid green;
  color: green;
}

.delete {
  border: 2px solid red;
  color: red;
}

.logout, .details, .renew {
  border: 2px solid black;
  color: black;
}

.left-part {
  width: 90%;
  overflow-y: auto;
}

.header {
  height: 20%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}

.buttons {
  border-top: 2px solid black;
  height: 20%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

@media (max-width: 768px) {
  .buttons {
    display: flex;
    flex-direction: column;
    height: 40%;
  }

  .buttons > * {
    width: 60%;
    height: 30%;
    font-size: 2vh;
  }

  .field {
    width: 80%;
    height: 40%;
  }

  .circle {
    width: 4vh;
    height: 4vh;
    border-radius: 50%;
    border: 2px solid black;
  }

  .model-config, .header, .user-verify {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .model-config, .header {
    overflow-y: auto;
  }

  .toggle-button {
    height: 30%;
  }

  .models {
    width: 90%;
    height: auto;
  }

  h3, .field, .details, .logout {
    font-size: 1.5vh;
  }

  .info {
    font-size: 1.25vh;
  }

  .logout {
    width: 60%;
    height: 30%;
  }
}
</style>