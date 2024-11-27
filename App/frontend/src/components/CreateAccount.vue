<script setup>
import {ref, watch} from "vue";
import FormTextField from "@/components/FormTextField.vue";
import FormRadioField from "@/components/FormRadioField.vue";
import axios from "axios";
import Error from "@/components/Error.vue";

const name = ref('')
const username = ref('')
const email = ref('')
const password = ref('')
const usertype = ref(0)

const errors = ref([])

const createAccount = async () => {
  const sub_num = [10, 30, 100][+usertype.value] || 10
  try {
    const response = await axios.post('http://localhost:8000/api/user/create_user', {
      name: name.value,
      email: email.value,
      username: username.value,
      usertype: +usertype.value,
      password: password.value,
      submission_num: sub_num
    })

    resetInputs()
  } catch (e) {
    const error_response = e.response.data
    if (typeof error_response['error'] === 'string') {
      errors.value = [error_response['error']]
    } else if (typeof error_response['error'] === 'undefined') {
      errors.value = ['BŁĄD!! Nie udało się połączyć z serwerem.']
    } else {
      errors.value = error_response['error']
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
  <Error v-model="errors" v-if="errors.length !== 0"></Error>
  <div class="left-part" :style="{
    opacity: errors.length === 0 ? '1' : '0.3',
    pointerEvents: errors.length === 0 ? 'auto' : 'none'
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
            v-model="name"
            :label_info="'Imię i nazwisko'"
            :label_name="'name'"
        ></FormTextField>

        <FormTextField
            v-model="username"
            :label_info="'Nazwa użytkownika'"
            :label_name="'username'"
        ></FormTextField>

        <FormTextField
            v-model="email"
            :label_info="'Email'"
            :label_name="'email'"
        ></FormTextField>

        <FormTextField
            v-model="password"
            :label_info="'Hasło'"
            :label_name="'password'"
        ></FormTextField>

        <FormRadioField v-model="usertype"></FormRadioField>

        <div class="buttons" style="border: none; height: 100px">
          <button type="submit" class="router-link">Wyślij</button>
          <button type="button" class="router-link" @click="resetInputs()">Wyczyść</button>
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
}

.left-part {
  width: 90%;
}

.form {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

form {
  border-top: 2px solid black;
  width: 100%;
  height: 60%;
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
  justify-content: space-evenly;
  align-items: center;
}

.buttons > * {
  font-size: 1.5vw;
}

@media (max-width: 900px) {
  .buttons > * {
    width: 100%;
  }

  .header, .error {
    font-size: 1.75vh;
  }
}
</style>