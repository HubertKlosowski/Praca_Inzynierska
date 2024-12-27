<script setup>
import {reactive, ref} from "vue";
import FormTextField from "@/components/FormTextField.vue";
import ResponseOutput from "@/components/ResponseOutput.vue";
import axios from "axios";
import _ from "lodash";
import {useRouter} from "vue-router";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import FormButtonField from "@/components/FormButtonField.vue";


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
      :after_create="after_create"
      v-if="response_status >= 200"
      :move_to="'/profile'"
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
    <div class="go-main">
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