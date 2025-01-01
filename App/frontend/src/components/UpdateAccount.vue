<script setup>
import {reactive, ref} from "vue";
import FormTextField from "@/components/FormTextField.vue";
import ResponseOutput from "@/components/ResponseOutput.vue";
import axios from "axios";
import _ from "lodash";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import FormButtonField from "@/components/FormButtonField.vue";


const show_password = ref(false)
const form_fields = reactive({
  name: '',
  username: '',
  email: '',
  password: ''
})
const logged_user = reactive(JSON.parse(localStorage.getItem('user')))

const after_create = ref({})
const title = ref('')
const subtitle = ref('')
const response_status = ref(0)
const token = reactive(JSON.parse(localStorage.getItem('token')))


const updateAccount = async () => {
  try {
    const data = _.pickBy(form_fields, value => value && value.length > 0)
    const response = await axios.patch(
        'http://localhost:8000/api/user/update_user',
        data,
        {headers: {'Authorization' : `Bearer ${token['access']}`}})

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

    localStorage.setItem('user', JSON.stringify(user))
    resetInputs()

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
      subtitle.value = 'Próba zmiany danych użytkownika się nie powiodła. Proszę zapoznać się z komunikatami wyświetlanymi poniżej:'

      if (response_status.value === 429) {
        title.value = 'Przekroczony limit zmian danych użytkownika'
      } else if (response_status.value === 403) {
        title.value = 'Problem z weryfikacją użytkownika'
        if (error_response.data.code === 'access_token_failed') {  // jeśli access_token wygaśnie
          await refreshAccessToken(['Twoje dane wygasły, ale zostały odświeżone.', 'Teraz możesz zmienić dane użytkownika.'])
        }
      } else {
        title.value = 'Problem z danymi'
      }
    }
  }
}

const refreshAccessToken = async (after_create_success) => {
  try {
    const response = await axios.post('http://localhost:8000/api/token/refresh', {
      'refresh': token['refresh']
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

const resetInputs = () => {
  form_fields.name = ''
  form_fields.username = ''
  form_fields.email = ''
  form_fields.password = ''
}
</script>

<template>

  <ResponseOutput
      v-model:response_status="response_status"
      :after_create="after_create"
      v-if="response_status >= 100 && response_status !== 403"
      :move_to="'/profile'"
      :title="title"
      :subtitle="subtitle"
  ></ResponseOutput>

  <div class="left-part" :style="{
    opacity: response_status >= 100 && response_status !== 403 ? '0.3' : '1',
    pointerEvents: response_status >= 100 && response_status !== 403 ? 'none' : 'auto'
  }">
    <div class="header">
      <h3>Zmień dane konta</h3>
      <ul>
        <li>Nie wymagana jest zmiana wszystkich pól.</li>
        <li>Typu użytkownika nie można zmienić, ze względu bezpieczeństwa.</li>
      </ul>
    </div>
    <div class="go-main">
      <RouterLink to="/profile" class="router-link">
        <font-awesome-icon :icon="['fas', 'user']" />
      </RouterLink>
    </div>
    <div class="form">
      <form @submit.prevent="updateAccount">

        <FormTextField
            v-model:input_value="form_fields.name"
            :label_info="'imię i nazwisko'"
            :input_placeholder="logged_user.name"
            :label_name="'name'"
        ></FormTextField>

        <FormTextField
            v-model:input_value="form_fields.username"
            :label_info="'nazwę użytkownika'"
            :input_placeholder="logged_user.username"
            :label_name="'username'"
        ></FormTextField>

        <FormTextField
            v-model:input_value="form_fields.email"
            :label_info="'email'"
            :input_placeholder="logged_user.email"
            :label_name="'email'"
        ></FormTextField>

        <FormTextField
            v-model:input_value="form_fields.password"
            v-model:show_password="show_password"
            :label_info="'hasło'"
            :input_placeholder="'Wiesz jakie masz hasło 🙂'"
            :label_name="'password'"
        ></FormTextField>

        <FormButtonField :login="false" @redEvent="() => { resetInputs() }">
          <template v-slot:green>
            Zatwierdź
          </template>
          <template v-slot:red>
            Wyczyść
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
  height: 70%;
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