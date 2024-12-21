<script setup>
import {reactive, ref} from "vue";
import FormTextField from "@/components/FormTextField.vue";
import ResponseOutput from "@/components/ResponseOutput.vue";
import axios from "axios";
import _ from "lodash";
import {useRouter} from "vue-router";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";


const router = useRouter()

const show_password = ref(false)
const new_user = reactive({
  name: '',
  username: '',
  email: '',
  password: ''
})
const logged_user = ref(JSON.parse(localStorage.getItem('user')))

const after_create = ref({})
const title = ref('')
const subtitle = ref('')
const response_status = ref(0)


const updateAccount = async () => {
  try {
    const response = await axios.patch(
        'http://localhost:8000/api/user/update_user/' + logged_user.value['username'],
        _.pickBy(new_user, value => value && value.length > 0)
    )

    after_create.value = response.data.user
    title.value = response.data.success
    subtitle.value = ''
    response_status.value = response.status

    localStorage.setItem('user', JSON.stringify(after_create.value))
    await router.push('/profile')
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
  new_user.name = ''
  new_user.username = ''
  new_user.email = ''
  new_user.password = ''
}

const goHome = async () => {
  await router.push('/')
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
      <div class="content">
        <h3>Zmień dane konta</h3>
        <ul>
          <li>Nie wymagana jest zmiana wszystkich pól.</li>
          <li>Typu użytkownika nie można zmienić, ze względu bezpieczeństwa.</li>
        </ul>
      </div>
      <font-awesome-icon :icon="['fas', 'house']" class="router-link" @click="goHome" />
    </div>
    <div class="form">
      <form @submit.prevent="updateAccount">

        <FormTextField
            v-model:input_value="new_user.name"
            :label_info="'imię i nazwisko'"
            :input_placeholder="logged_user['name']"
            :label_name="'name'"
        ></FormTextField>

        <FormTextField
            v-model:input_value="new_user.username"
            :label_info="'nazwę użytkownika'"
            :input_placeholder="logged_user['username']"
            :label_name="'username'"
        ></FormTextField>

        <FormTextField
            v-model:input_value="new_user.email"
            :label_info="'email'"
            :input_placeholder="logged_user['email']"
            :label_name="'email'"
        ></FormTextField>

        <FormTextField
            v-model:input_value="new_user.password"
            v-model:show_password="show_password"
            :label_info="'hasło'"
            :input_placeholder="'Wiesz jakie masz hasło 🙂'"
            :label_name="'password'"
        ></FormTextField>

        <div class="form-row">
          <button type="submit" class="update">Zatwierdź</button>
          <button type="button" class="delete" @click="resetInputs">Wyczyść</button>
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

.router-link {
  width: 10%;
  height: 20%;
  padding: 1rem;
}

.update, .delete {
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

.update:hover, .delete:hover {
  color: white;
  border: 2px solid white;
  box-shadow: 0.5rem 0.5rem dodgerblue;
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

@media (max-width: 768px) {
  .form-row > * {
    width: 70%;
    font-size: 1.75vh;
  }

  .header {
    font-size: 1.75vh;
  }
}
</style>