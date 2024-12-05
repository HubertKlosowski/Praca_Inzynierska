<script setup>
import {ref} from "vue";
import FormTextField from "@/components/FormTextField.vue";
import FormRadioField from "@/components/FormRadioField.vue";
import ResponseOutput from "@/components/ResponseOutput.vue";
import axios from "axios";

const name = ref('')
const username = ref('')
const email = ref('')
const password = ref('')
const usertype = ref(0)

const after_create = ref({})
const title = ref('')
const response_status = ref(0)
const show_password = ref(false)

const createAccount = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/user/create_user', {
      name: name.value,
      email: email.value,
      username: username.value,
      usertype: +usertype.value,
      password: password.value
    })

    after_create.value = response.data.user
    title.value = response.data.success
    response_status.value = response.status

    resetInputs()

  } catch (e) {
    if (typeof e.response === 'undefined') {
      after_create.value = ['BŁĄD!! Nie udało się połączyć z serwerem.']
      response_status.value = 500
      title.value = 'Problem z serwerem'
    } else {
      const error_response = e.response
      after_create.value = error_response.data.error
      response_status.value = error_response.status
      title.value = 'Problem z podanymi danymi'
    }
  }
}

const resetInputs = () => {
  name.value = ''
  username.value = ''
  email.value = ''
  password.value = ''
  usertype.value = 0
}
</script>

<template>

  <ResponseOutput
      v-model:response_status="response_status"
      v-model:after_create="after_create"
      v-if="response_status >= 200"
      :title="title"
  ></ResponseOutput>

  <div class="left-part" :style="{
    opacity: response_status < 200 ? '1' : '0.3',
    pointerEvents: response_status < 200 ? 'auto' : 'none'
  }">
    <div class="header">
      <h3>Utwórz konto</h3>
      <ul>
        <li>Poniżej znajduje się formularz, w którym należy podać własne dane osobowe.</li>
        <li>Wszystkie pola muszą być wypełnione aby móc utworzyć konto.</li>
        <li>Konto służy do przechowywania wyników analiz i zarządzania.</li>
      </ul>
    </div>
    <div class="form">
      <form @submit.prevent="createAccount">

        <FormTextField
            v-model:input_value="name"
            :label_info="'imię i nazwisko'"
            :input_placeholder="'Imię i nazwisko'"
            :label_name="'name'"
        ></FormTextField>

        <FormTextField
            v-model:input_value="username"
            :label_info="'nazwę użytkownika'"
            :input_placeholder="'Nazwa użytkownika'"
            :label_name="'username'"
        ></FormTextField>

        <FormTextField
            v-model:input_value="email"
            :label_info="'Email'"
            :input_placeholder="'Adres email'"
            :label_name="'email'"
        ></FormTextField>

        <FormTextField
            v-model:input_value="password"
            v-model:show_password="show_password"
            :label_info="'Hasło'"
            :input_placeholder="'Hasło'"
            :label_name="'password'"
        ></FormTextField>

        <FormRadioField v-model="usertype"></FormRadioField>

        <div class="buttons" style="border: none; height: 100px">
          <button type="submit" class="router-link">Wyślij</button>
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