<script setup>
import {reactive, ref} from "vue";
import FormTextField from "@/components/FormTextField.vue";
import axios from "axios";
import _ from "lodash";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import FormButtonField from "@/components/FormButtonField.vue";
import router from "@/router/index.js";
import ResponseOutput from "@/components/ResponseOutput.vue";


const username = ref('')
const password = ref('')
const users_verify = ref([])
const show_password = ref(false)
const token = reactive({
  access: '',
  refresh: ''
})

const after_create = ref({})
const title = ref('')
const subtitle = ref('')
const response_status = ref(0)


const login = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/user/login_user', {
      username: username.value,
      password: password.value
    })

    const tmp = response.data
    token.access = tmp['access']
    token.refresh = tmp['refresh']

    localStorage.setItem('token', JSON.stringify(tmp))

  } catch (e) {
    if (typeof e.response === 'undefined') {
      after_create.value = ['Nie udało się połączyć z serwerem.']
      response_status.value = 500
      title.value = 'Problem z serwerem'
      subtitle.value = 'Proszę poczekać, serwer nie jest teraz dostępny.'
    } else {
      const error_response = e.response
      response_status.value = error_response.status

      if (response_status.value === 429) {
        title.value = 'Przekroczony limit prób logowania'
      } else if (response_status.value === 403) {
        title.value = 'Problem z weryfikacją użytkownika'
      } else {
        title.value = 'Problem z danymi'
      }

      after_create.value = error_response.data.error
      subtitle.value = 'Próba logowania się nie powiodła. Proszę zapoznać się z komunikatami wyświetlanymi poniżej:'

      return
    }
  }

  try {
    const response = await axios.get('http://localhost:8000/api/user/get_user_data', {
      headers: {'Authorization' : 'Bearer ' + token['access']}
    })

    localStorage.setItem('history_submissions', JSON.stringify(response.data['submissions']))
    const user = response.data['user']
    const usertypes = ['Normal', 'Pro', 'Administrator']

    after_create.value = [
      ['Imię i nazwisko', user['name']],
      ['Nazwa użytkownika', user['username']],
      ['Adres email', user['email']],
      ['Typ konta', usertypes[user['usertype']]],
    ]
    title.value = response.data.success
    subtitle.value = ''
    response_status.value = response.status

    const date = new Date()
    localStorage.setItem('user', JSON.stringify(user))
    localStorage.setItem('session', JSON.stringify(date.setHours(date.getHours() + 1)))

    if (user['usertype'] === 2) {
      await getUsers(user)
    }
    resetInputs()
    await router.push('/profile')

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
      title.value = 'Problem z danymi'
      subtitle.value = 'Dane przekazane do formularza są błędne. Proszę je poprawić, zgodnie z komunikatami wyświetlanymi poniżej:'
    }
  }
}

const getUsers = async (user) => {
  try {
    const response = await axios.get('http://localhost:8000/api/get_users', {
      headers: {'Authorization' : 'Bearer ' + token['access']}
    })
    users_verify.value = _.remove(response.data, function (n) {
      return n['username'] !== user['username']
    })
    localStorage.setItem('users_verify', JSON.stringify(users_verify.value))

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
      title.value = 'Problem z dostępem do użytkowników'
      subtitle.value = 'Podczas zbierania informacji o użytkownikach wystąpił błąd. Poniżej podano przyczyny wystąpienia błędu:'
    }
  }
}

const resetInputs = () => {
  username.value = ''
  password.value = ''
}
</script>

<template>

  <ResponseOutput
      v-model:response_status="response_status"
      :after_create="after_create"
      v-if="response_status >= 400"
      :title="title"
      :subtitle="subtitle"
  ></ResponseOutput>

  <div class="left-part">
    <div class="header">
      <h3>Witaj ponownie</h3>
    </div>
    <div class="go-main">
      <RouterLink to="/" class="router-link">
        <font-awesome-icon :icon="['fas', 'house']" />
      </RouterLink>
    </div>
    <div class="form">
      <form @submit.prevent="login">

        <FormTextField
            v-model:input_value="username"
            :label_info="'nazwę użytkownika'"
            :input_placeholder="'Nazwa użytkownika'"
            :label_name="'username'"
        ></FormTextField>

        <FormTextField
            v-model:input_value="password"
            v-model:show_password="show_password"
            :label_info="'Hasło'"
            :input_placeholder="'Hasło'"
            :label_name="'password'"
        ></FormTextField>

        <FormButtonField :login="true">
          <template v-slot:green>
            Zaloguj się
          </template>
        </FormButtonField>

      </form>
    </div>
  </div>
</template>

<style scoped>
.go-main {
  width: 100%;
  height: 10%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  padding-top: 1rem;
}

.router-link {
  width: 10%;
  padding: 1rem;
}

li {
  list-style-type: '👉';
}

.header {
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
  font-size: 1.5vw;
}

.left-part {
  width: 90%;
}

.form {
  width: 100%;
  height: 80%;
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
}

form {
  width: 100%;
  margin: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
}

@media (max-width: 700px) {
  .header {
    font-size: 1.5vh;
  }
}
</style>