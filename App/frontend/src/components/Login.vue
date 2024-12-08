<script setup>
import {ref} from "vue";
import FormTextField from "@/components/FormTextField.vue";
import axios from "axios";
import ResponseOutput from "@/components/ResponseOutput.vue";
import {useRouter} from "vue-router";
import _ from "lodash";


const router = useRouter()

const username = ref('')
const password = ref('')
const users_verify = ref([])
const show_password = ref(false)
const user = ref({})

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

    after_create.value = response.data.user
    title.value = response.data.success
    subtitle.value = ''
    response_status.value = response.status

    localStorage.setItem('history_submissions', JSON.stringify(response.data['submissions']))
    user.value = response.data['user']

    localStorage.setItem('user', JSON.stringify(user.value))

    if (user.value['usertype'] === 2) {
      await getUsers()
    }
    resetInputs()
    await router.push('/profile')

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
      title.value = 'Problem z podanymi danymi'
      subtitle.value = 'Dane przekazane do formularza są błędne. Proszę je poprawić, zgodnie z komunikatami wyświetlanymi poniżej:'
    }
  }
}

const getUsers = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/get_users')
    users_verify.value = _.remove(response.data, function (n) {
      return n['username'] !== user.value['username']
    })
    localStorage.setItem('users_verify', JSON.stringify(users_verify.value))
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
      title.value = 'Problem z dostępem do użytkowników'
      subtitle.value = 'Podczas zbierania informacji o użytkownikach wystąpił błąd. Proszę je poprawić, zgodnie z komunikatami wyświetlanymi poniżej:'
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
      v-model:after_create="after_create"
      v-if="response_status >= 200"
      :title="title"
      :subtitle="subtitle"
  ></ResponseOutput>

  <div class="left-part" :style="{
    opacity: response_status < 200 ? '1' : '0.3',
    pointerEvents: response_status < 200 ? 'auto' : 'none'
  }">
    <div class="header">
      <h3>Witaj ponownie</h3>
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

        <div class="buttons" style="border: none;">
          <button type="submit" class="router-link">Zaloguj się</button>
        </div>
      </form>
    </div>
    <div class="buttons">
      <RouterLink to="/" class="router-link">Wróć do strony głównej</RouterLink>
    </div>
  </div>
</template>

<style scoped>
li {
  list-style-type: '👉';
}

.header {
  height: 10%;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  font-size: 1.5vw;
}

.left-part {
  width: 90%;
  overflow-y: hidden;
}

.form {
  width: 100%;
  height: 70%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

form {
  position: relative;
  width: 100%;
  height: 100%;
  margin: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow-y: auto;
}

.buttons {
  border-top: 2px solid black;
  width: 100%;
  height: 20%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.buttons > * {
  font-size: 1.5vw;
}

@media (max-width: 768px) {
  .buttons > * {
    width: 70%;
  }

  .router-link {
    font-size: 1.75vh !important;
  }

  .header {
    font-size: 1.75vh;
  }
}
</style>