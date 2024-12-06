<script setup>
import {inject, ref} from "vue";
import FormTextField from "@/components/FormTextField.vue";
import ResponseOutput from "@/components/ResponseOutput.vue";
import axios from "axios";
import _ from "lodash";

const $cookies = inject('$cookies')

const show_password = ref(false)
const name = ref('')
const username = ref('')
const email = ref('')
const password = ref('')
const logged_user = $cookies.get('user')

const after_create = ref({})
const title = ref('')
const subtitle = ref('')
const response_status = ref(0)

const updateAccount = async () => {
  try {
    let new_user = {
      name: name.value,
      email: email.value,
      username: username.value,
      password: password.value
    }

    new_user = _.pickBy(new_user, value => value && value.length > 0)

    const response = await axios.patch('http://localhost:8000/api/user/update_user/' + logged_user['username'], new_user)

    after_create.value = response.data.user
    title.value = response.data.success
    subtitle.value = ''
    response_status.value = response.status

    $cookies.set('user', after_create.value)

    resetInputs()
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

const resetInputs = () => {
  name.value = ''
  username.value = ''
  email.value = ''
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
      <h3>Zmień dane konta</h3>
      <ul>
        <li>Nie wymagana jest zmiana wszystkich pól.</li>
        <li>Typu użytkownika nie można zmienić, ze względu bezpieczeństwa.</li>
      </ul>
    </div>
    <div class="form">
      <form @submit.prevent="updateAccount">

        <FormTextField
            v-model:input_value="name"
            :label_info="'imię i nazwisko'"
            :input_placeholder="logged_user['name']"
            :label_name="'name'"
        ></FormTextField>

        <FormTextField
            v-model:input_value="username"
            :label_info="'nazwę użytkownika'"
            :input_placeholder="logged_user['username']"
            :label_name="'username'"
        ></FormTextField>

        <FormTextField
            v-model:input_value="email"
            :label_info="'email'"
            :input_placeholder="logged_user['email']"
            :label_name="'email'"
        ></FormTextField>

        <FormTextField
            v-model:input_value="password"
            v-model:show_password="show_password"
            :label_info="'hasło'"
            :input_placeholder="'Wiesz jakie masz hasło 🙂'"
            :label_name="'password'"
        ></FormTextField>

        <div class="buttons" style="border: none">
          <button type="submit" class="router-link">Zatwierdź</button>
          <button type="button" class="router-link" @click="resetInputs">Wyczyść</button>
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
  height: 20%;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  font-size: 1.5vw;
  padding-bottom: 1rem;
}

.left-part {
  width: 90%;
}

.form {
  width: 100%;
  height: 60%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

form {
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
  height: 15%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}

.buttons > * {
  font-size: 1.5vw;
}

@media (max-width: 768px) {
  .buttons > * {
    width: 70%;
    font-size: 1.75vh;
  }

  .header {
    font-size: 1.75vh;
  }
}
</style>