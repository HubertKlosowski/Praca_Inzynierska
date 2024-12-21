<script setup>
import {reactive, ref} from "vue";
import FormTextField from "@/components/FormTextField.vue";
import FormRadioField from "@/components/FormRadioField.vue";
import ResponseOutput from "@/components/ResponseOutput.vue";
import axios from "axios";
import {useRouter} from "vue-router";


const router = useRouter()

const user = reactive({
  name: '',
  email: '',
  username: '',
  usertype: 0,
  password: ''
})

const after_create = ref({})
const title = ref('')
const subtitle = ref('')
const response_status = ref(0)
const show_password = ref(false)


const createAccount = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/user/create_user', user)

    after_create.value = [user.username, user.email]
    title.value = response.data.success
    subtitle.value = ''
    response_status.value = response.status
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
  user.name = ''
  user.email = ''
  user.username = ''
  user.usertype = 0
  user.password = ''
}

const goHome = async () => {
  await router.push('/')
}
</script>

<template>

  <ResponseOutput
      v-model:response_status="response_status"
      v-model:after_create="after_create"
      :move_to="'/'"
      v-if="response_status >= 200"
      :title="title"
      :subtitle="subtitle"
  ></ResponseOutput>

  <div class="left-part" :style="{
    opacity: response_status < 200 ? '1' : '0.3',
    pointerEvents: response_status < 200 ? 'auto' : 'none'
  }">
    <div class="header">
      <div class="content">
        <h3>Utwórz konto</h3>
        <ul>
          <li>Poniżej znajduje się formularz, w którym należy podać własne dane osobowe.</li>
          <li>Wszystkie pola muszą być wypełnione aby móc utworzyć konto.</li>
          <li>Konto służy do przechowywania wyników analiz i zarządzania.</li>
        </ul>
      </div>
      <font-awesome-icon :icon="['fas', 'house']" class="router-link" @click="goHome" />
    </div>
    <div class="form">
      <form @submit.prevent="createAccount">

        <FormTextField
            v-model:input_value="user.name"
            :label_info="'imię i nazwisko'"
            :input_placeholder="'Imię i nazwisko'"
            :label_name="'name'"
        ></FormTextField>

        <FormTextField
            v-model:input_value="user.username"
            :label_info="'nazwę użytkownika'"
            :input_placeholder="'Nazwa użytkownika'"
            :label_name="'username'"
        ></FormTextField>

        <FormTextField
            v-model:input_value="user.email"
            :label_info="'Email'"
            :input_placeholder="'Adres email'"
            :label_name="'email'"
        ></FormTextField>

        <FormTextField
            v-model:input_value="user.password"
            v-model:show_password="show_password"
            :label_info="'Hasło'"
            :input_placeholder="'Hasło'"
            :label_name="'password'"
        ></FormTextField>

        <FormRadioField v-model="user.usertype"></FormRadioField>

        <div class="form-row">
          <button type="submit" class="create">Utwórz</button>
          <button type="button" class="reset" @click="resetInputs">Wyczyść</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 80%;
}

.left-part {
  width: 90%;
}

.router-link {
  width: 10%;
  height: 20%;
  padding: 1rem;
}

li {
  list-style-type: '👉';
}

.header {
  height: 20%;
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  font-size: 1.5vw;
  padding-bottom: 1rem;
}

.left-part {
  width: 90%;
}

.form {
  width: 100%;
  height: 80%;
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
}

.form-row {
  width: 80%;
  height: 20%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
  border-radius: 0.75rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.7);
  margin: 1rem;
  padding: 1rem;
}

.create, .reset {
  text-decoration: none;
  text-align: center;
  align-content: center;
  margin: 1rem;
  font-size: 1.25vw;
  transition: 0.4s ease;
  cursor: pointer;
  background-color: white;
  border-radius: 1rem;
  width: 40%;
  height: 70%;
}

.create:hover, .reset:hover {
  color: white;
  border: 2px solid white;
  box-shadow: 0.5rem 0.5rem dodgerblue;
}

.create:hover {
  background-color: darkgreen;
}

.reset:hover {
  background-color: darkred;
}

.create {
  border: 2px solid green;
  color: green;
}

.reset {
  border: 2px solid red;
  color: red;
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