<script setup>
import {inject, onMounted, reactive, ref} from "vue";
import english from "@/assets/angielski.png";
import {useRouter} from "vue-router";
import axios from "axios";
import ResponseOutput from "@/components/ResponseOutput.vue";
import AdminPanel from "@/components/AdminPanel.vue";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import FormButtonField from "@/components/FormButtonField.vue";
import FormTextField from "@/components/FormTextField.vue";


const router = useRouter()
const $cookies = inject('$cookies')

const user = ref(JSON.parse(localStorage.getItem('user')))
const usertypes = ref(['Normal', 'Pro', 'Administrator'])

const choose_model = ref(false)
const history_submissions = ref(JSON.parse(localStorage.getItem('history_submissions')))
const new_name = ref('')
const change_name = ref(-1)

const model = ref('')

const after_create = ref({})
const title = ref('')
const subtitle = ref('')
const response_status = ref(0)
const token = reactive(JSON.parse(localStorage.getItem('token')))


const logoutUser = async () => {
  localStorage.clear()
  localStorage.setItem('choosen_model', JSON.stringify('bert-base'))
  $cookies.remove('made_submission')
  await router.push('/')
}

const setEnglishModel = () => {
  choose_model.value = !choose_model.value
  model.value = choose_model.value ? 'bert-large' : 'bert-base'
  localStorage.setItem('choosen_model', JSON.stringify(model.value))
}

const showDetails = async (submission) => {
  try {
    const response = await axios.get(
        'http://localhost:8000/api/submission/get_submission/' + submission['id'],
        {headers: {'Authorization' : `Bearer ${token['access']}`}}
    )
    localStorage.setItem('depressed', JSON.stringify(response.data['depressed']))
    localStorage.setItem('text', JSON.stringify(response.data['text']))
    localStorage.setItem('choosen_submission', JSON.stringify(submission))
    await router.push('/predict')

  } catch (e) {
    if (typeof e.response === 'undefined') {
      after_create.value = ['Nie udało się połączyć z serwerem.']
      response_status.value = 500
      title.value = 'Problem z serwerem'
      subtitle.value = 'Proszę poczekać, serwer nie jest teraz dostępny.'
    } else {
      const error_response = e.response
      response_status.value = error_response.status
      after_create.value = error_response.data.error
      subtitle.value = 'Podczas wyszukiwania rezultatów wystąpił błąd. Proszę zapoznać się z błędem podanym poniżej i spróbować ponownie.'

      if (response_status.value === 429) {
        title.value = 'Przekroczony limit zmian danych użytkownika'
      } else if (response_status.value === 403) {
        title.value = 'Problem z weryfikacją użytkownika'
        if (error_response.data.code === 'access_token_failed') {  // jeśli access_token wygaśnie
          await refreshAccessToken(['Twoje dane wygasły, ale zostały odświeżone.', 'Teraz możesz wyświetlić szczegóły próby.'])
        }
      } else {
        title.value = 'Problem z danymi'
      }
    }
  }
}

const setPredictionName = async (submission, num) => {
  change_name.value = -1
  try {
    await axios.patch(
        'http://localhost:8000/api/submission/change_name/' + submission['id'],
        {'name': new_name.value},
        {headers: {'Authorization' : `Bearer ${token['access']}`}}
    )
    history_submissions.value[num]['name'] = new_name.value
    localStorage.setItem('history_submissions', JSON.stringify(history_submissions.value))
    new_name.value = ''

  } catch (e) {
    if (typeof e.response === 'undefined') {
      after_create.value = ['Nie udało się połączyć z serwerem.']
      response_status.value = 500
      title.value = 'Problem z serwerem'
      subtitle.value = 'Proszę poczekać, serwer nie jest teraz dostępny.'
    } else {
      const error_response = e.response
      after_create.value = error_response.data.error
      response_status.value = error_response.status
      subtitle.value = 'Podczas zmiany nazwy próby wystąpił błąd.'

      if (response_status.value === 429) {
        title.value = 'Przekroczony limit zmian danych użytkownika'
      } else if (response_status.value === 403) {
        title.value = 'Problem z weryfikacją użytkownika'
        if (error_response.data.code === 'access_token_failed') {  // jeśli access_token wygaśnie
          await refreshAccessToken(['Twoje dane wygasły, ale zostały odświeżone.', 'Teraz możesz ustawić nazwę próby.'])
        }
      } else {
        title.value = 'Problem z danymi'
      }
    }
  }
}

const refreshAccessToken = async (after_create_success) => {
  try {
    const response = await axios.post(
        'http://localhost:8000/api/token/refresh',
        {'refresh': token.refresh}
    )

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

const goHome = async () => {
  await router.push('/')
}

const closeWindow = () => {
  change_name.value = -1
}

onMounted(() => {
  console.log(localStorage.getItem('choosen_model'))
  if (localStorage.getItem('choosen_model') === null) {
    localStorage.setItem('choosen_model', JSON.stringify('bert-base'))
    console.log('nie ma w localStorage: ', JSON.parse(localStorage.getItem('choosen_model')))
  } else {
    model.value = JSON.parse(localStorage.getItem('choosen_model'))
    choose_model.value = model.value !== 'bert-base'
    console.log('jest w localStorage: ', JSON.parse(localStorage.getItem('choosen_model')))
  }
  console.log(model.value)
})
</script>

<template>

  <ResponseOutput
      v-model:response_status="response_status"
      :after_create="after_create"
      v-if="response_status >= 100 && response_status !== 403"
      :title="title"
      :subtitle="subtitle"
  ></ResponseOutput>

  <div class="left-part" :style="{
    opacity: response_status >= 100 && response_status !== 403 ? '0.3' : '1',
    pointerEvents: response_status >= 100 && response_status !== 403 ? 'none' : 'auto'
  }" v-else>
    <div class="header">
      <div class="title">
        <h3>Witaj {{ user['username'] }}!</h3>
      </div>
      <div class="rest">
        <button type="button" class="logout" @click="logoutUser">Wyloguj się</button>
      </div>
    </div>
    <div class="account-details">
      <div class="title">
        <h3>Szczegóły konta</h3>
      </div>
      <div class="rest">
        <div class="info">
          <span style="font-weight: bold">Imię i nazwisko</span>
          <span>{{ user['name'] }}</span>
        </div>
        <div class="info">
          <span style="font-weight: bold">Adres email</span>
          <span>{{ user['email'] }}</span>
        </div>
        <div class="info">
          <span style="font-weight: bold">Typ konta</span>
          <span>{{ usertypes[user['usertype']] }}</span>
        </div>
        <div class="info">
          <span style="font-weight: bold">Dzienne próby</span>
          <span>{{ user['submission_num'] }}</span>
        </div>
      </div>
    </div>
    <div class="model-config">
      <div class="title">
        <h3>Konfiguracja modelu</h3>
      </div>
      <div class="rest">
        <h3>LARGE</h3>
        <div class="t-buttons">
          <div
              class="toggle-button"
              :style="{ justifyContent: choose_model ? 'start' : 'end' }"
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
      <div class="header-history">
        <div class="field" style="width: 10%">Numer</div>
        <div class="field">Nazwa</div>
        <div class="field">Szczegóły</div>
      </div>
      <div class="h-submissions">
        <div class="history-submission" v-for="(item, i) in history_submissions" :key="item" v-if="history_submissions.length !== 0">
          <div class="field" style="width: 10%">{{ i + 1 }}</div>
          <div class="field" @click="change_name = i" v-if="item.name !== null" v-show="change_name !== i">{{ item.name }}</div>
          <div class="field" @click="change_name = i" v-else v-show="change_name !== i">Brak nazwy</div>
          <div class="field" v-if="change_name === i" style="overflow-y: auto; align-items: start;">
            <form @submit.prevent="setPredictionName(item, i)">

              <FormTextField
                  v-model:input_value="new_name"
                  :minimize="true"
                  :label_info="''"
                  :input_placeholder="item.name"
                  :label_name="''"
              ></FormTextField>

              <FormButtonField :login="false" @redEvent="() => { closeWindow() }">
                <template v-slot:green>
                  <font-awesome-icon :icon="['fas', 'check']" />
                </template>
                <template v-slot:red>
                  <font-awesome-icon :icon="['fas', 'xmark']" />
                </template>
              </FormButtonField>

            </form>
          </div>
          <div class="field" style="border: none">
            <button type="button" class="details" @click="showDetails(item)">Pokaż szczegóły</button>
          </div>
        </div>
        <div class="history-submission" v-else>
          Brak wykonanych prób
        </div>
      </div>
    </div>

    <AdminPanel
        v-if="user['usertype'] === 2"
        :usertypes="usertypes"
        v-model:after_create="after_create"
        v-model:title="title"
        v-model:response_status="response_status"
        v-model:subtitle="subtitle"
    ></AdminPanel>

    <div class="buttons">
      <RouterLink to="/update" class="update">Zmień dane</RouterLink>
      <RouterLink to="/delete" class="delete">Usuń konto</RouterLink>
      <font-awesome-icon :icon="['fas', 'house']" class="router-link" @click="goHome" />
    </div>
  </div>
</template>

<style scoped>
form {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

form > .update {
  width: 50%;
  height: 80%;
  font-size: 1.5vw;
}

form > input {
  width: 50%;
  height: 20%;
  box-sizing: border-box;
  padding: 1rem;
  border-radius: 0.75rem;
}

.history {
  border-top: 2px solid black;
  height: 60%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.h-submissions {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
  overflow-y: scroll;
  scrollbar-gutter: stable both-edges;
}

.history-submission {
  width: 90%;
  min-height: 70%;
  font-size: 1.5vw;
}

.header-history {
  width: calc(90% - 24px);
  min-height: 20%;
}

.history-submission, .header-history {
  margin: 1rem 0 1rem 0;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
  background-color: #f5f5f5;
  border-radius: 0.75rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.7);
}

.history-submission > * {
  overflow-y: hidden;
  overflow-x: auto;
  border-right: 2px solid black;
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
  width: 30%;
  height: 50%;
}

.details {
  width: 80%;
  height: 60%;
}

.buttons > * {
  width: 20%;
  height: 50%;
  padding: 1rem;
}

.update, .delete, .logout, .details {
  text-decoration: none;
  text-align: center;
  align-content: center;
  margin: 1rem;
  font-size: 1.5vw;
  transition: 0.4s ease;
  cursor: pointer;
  background-color: white;
  border-radius: 1rem;
}

.update:hover, .delete:hover, .logout:hover, .details:hover {
  color: white;
  border: 2px solid white;
  box-shadow: 0.5rem 0.5rem dodgerblue;
}

.details:hover, .logout:hover {
  background-color: black;
}

.update:hover {
  background-color: darkgreen;
}

.delete:hover {
  background-color: darkred;
}

.update {
  border: 2px solid green;
  color: green;
}

.delete {
  border: 2px solid red;
  color: red;
}

.logout, .details {
  border: 2px solid black;
  color: black;
}

.left-part {
  width: 90%;
}

.account-details, .model-config {
  border-top: 2px solid black;
  height: 20%;
}

.header, .account-details, .model-config {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
}

.header {
  height: 15%;
}

.title, .rest {
  height: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}

.title {
  width: 30%;
}

.rest {
  width: 70%;
}

.account-details > .rest {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  overflow-y: scroll;
  scrollbar-gutter: both-edges stable;
}

.info {
  margin: 0.5rem 0 0.5rem 0;
  width: 90%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  background-color: #f5f5f5;
  border-radius: 0.75rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.7);
}

.buttons {
  padding-top: 1rem;
  border-top: 2px solid black;
  height: 20%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

@media (max-width: 700px) {
  .buttons {
    display: flex;
    flex-direction: column;
    height: 40%;
  }

  .buttons > * {
    width: 50%;
    height: 10%;
    font-size: 2vh;
    padding: 1rem;
  }

  .header-history, .history-submission {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .field {
    width: 80%;
    height: 40%;
    border: none;
  }

  .circle {
    width: 4vh;
    height: 4vh;
    border-radius: 50%;
    border: 2px solid black;
  }

  .model-config, .header, .account-details {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    overflow-y: auto;
    overflow-x: hidden;
  }

  .model-config > .rest {
    display: flex;
    flex-direction: row;
    justify-content: space-evenly;
    align-items: center;
  }

  .title, .rest {
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    align-items: center;
  }

  .title {
    height: 20%;
  }

  .rest {
    height: 80%;
  }

  h3, .field, .details, .logout, .history-submission {
    font-size: 1.5vh;
  }

  span {
    font-size: 1.5vh;
  }

  .logout {
    width: 60%;
    height: 30%;
  }

  form {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  form > .update {
    width: 90%;
    height: 50%;
    font-size: 1.5vh;
  }

  form > input {
    width: 90%;
    height: 30%;
    font-size: 1.5vh;
  }
}

@media (max-width: 500px) {
  .account-details > .rest {
    display: grid;
    grid-template-columns: repeat(1, 1fr);
    overflow-y: scroll;
    scrollbar-gutter: both-edges stable;
  }
}

@media (max-height: 768px) {
  form {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
  }

  form > .update {
    width: 50%;
    height: 100%;
    font-size: 1.5vw;
  }

  form > input {
    width: 30%;
    height: 100%;
    font-size: 1.5vw;
  }
}
</style>