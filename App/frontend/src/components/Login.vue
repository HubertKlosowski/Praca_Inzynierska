<script setup>
import {inject, ref} from "vue";
import FormTextField from "@/components/FormTextField.vue";
import axios from "axios";
import ResponseOutput from "@/components/ResponseOutput.vue";

const $cookies = inject('$cookies')

const username = ref('')
const password = ref('')

const after_create = ref({})
const title = ref('')
const response_status = ref(0)

const login = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/user/login_user', {
      username: username.value,
      password: password.value
    })

    after_create.value = response.data.user
    title.value = response.data.success
    response_status.value = response.status

    $cookies.set('user', response.data.user)

    resetInputs()
  } catch (e) {
    title.value = e.response.data.success
    response_status.value = e.response.status

    const error_response = e.response.data
    if (typeof error_response['error'] === 'string') {
      after_create.value = error_response['error']
    } else if (typeof error_response['error'] === 'undefined') {
      after_create.value = ['BŁĄD!! Nie udało się połączyć z serwerem.']
    } else {
      after_create.value = error_response['error']
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
            v-model="username"
            :label_info="'Nazwę użytkownika'"
            :label_name="'username'"
        ></FormTextField>

        <FormTextField
            v-model="password"
            :label_info="'Hasło'"
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
    font-size: 3vh !important;
  }

  .header {
    font-size: 3vh;
  }
}
</style>