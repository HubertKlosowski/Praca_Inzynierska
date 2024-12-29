<script setup>
import {inject, onMounted, ref, watch} from "vue";
import {useRouter} from "vue-router";
import axios from "axios";
import ResponseOutput from "@/components/ResponseOutput.vue";
import _ from "lodash";
import CreateFileOutput from "@/components/CreateFileOutput.vue";
import FormButtonField from "@/components/FormButtonField.vue";
import FormTextAreaField from "@/components/FormTextAreaField.vue";
import FormFileField from "@/components/FormFileField.vue";


const router = useRouter()
const $cookies = inject('$cookies')

const show_loading_screen = defineModel('show_loading_screen')
const show_popup = defineModel('show_popup')
const send_creator = ref(false)
const user = ref(JSON.parse(localStorage.getItem('user')))
const choose = ref(true)
const data = ref(null)
const is_dragging = ref(false)
const model = ref('bert-base')

const after_create = ref({})
const title = ref('')
const subtitle = ref('')
const response_status = defineModel('response_status')


const makePredictions = async () => {
  if (_.isEmpty(user.value)) {
    await makeSubmissionAnon()
  } else {
    await makeSubmissionUser()
  }
}

const fromFileToData = () => {
  let to_csv = JSON.parse(localStorage.getItem('to_file'))
    to_csv.unshift('text')
    to_csv = to_csv.join('\n')

    try {
      data.value = new File([to_csv], 'creator.csv', {
        type: 'text/csv'
      })
    } catch (e) {
      after_create.value = ['Przekazane dane są niepoprawne!']
      response_status.value = 400
      title.value = 'Problem z danymi'
      subtitle.value = 'Proszę poprawić wprowadzone dane w kreatorze.'
    }
    localStorage.removeItem('to_file')
}

const checkData = () => {
  if (data.value === null || (typeof data.value === 'string' && data.value.length === 0)) {
    after_create.value = ['Przekazane dane są puste!']
    response_status.value = 400
    title.value = 'Problem z danymi'
    subtitle.value = 'Modele nie są w stanie pracować na pustych danych. Proszę przesłać plik lub tekst.'
    return false
  } else if (typeof data.value === 'object') {
    const extension = data.value.name.split('.')[1]
    if (extension !== 'csv' && extension !== 'json') {
      data.value = null
      after_create.value = ['Modele obsługują pliki z rozszerzeniem csv lub json.']
      response_status.value = 403
      title.value = 'Problem z danymi'
      subtitle.value = 'Nieprawidłowe rozszerzenie pliku. Proszę poprawić nazwę pliku i spróbować ponownie go przesłać.'
      return false
    } else if (data.value.size > 10000 && _.isEmpty(user.value)) {
      data.value = null
      after_create.value = ['Limit wielkości pliku dla gościa wynosi 100KB.']
      response_status.value = 403
      title.value = 'Problem z danymi'
      subtitle.value = 'Zbyt duży plik. Proszę przesłać plik o mniejszej wielkości.'
      return false
    }
  }
  return true
}

const handleErrorForSubmission = (error) => {
  show_loading_screen.value = false
  data.value = null

  if (typeof error.response === 'undefined' || error.status >= 500) {
    after_create.value = ['Nie udało się połączyć z serwerem.']
    response_status.value = 500
    title.value = 'Problem z serwerem'
    subtitle.value = 'Proszę poczekać, serwer nie jest teraz dostępny.'
  } else {
    const error_response = error.response
    after_create.value = error_response.data.error
    response_status.value = error_response.status
    title.value = 'Problem z danymi'
    subtitle.value = 'Przekazane dane zawierają błędy. Proszę się zapoznać z nimi i spróbować ponownie.'
  }
}

const makeSubmissionUser = async () => {
  if (localStorage.hasOwnProperty('to_file')) {
    fromFileToData()
  } else if (!checkData()) {
    return
  }

  let form_data = new FormData()
  form_data.append('content', data.value)
  form_data.append('model', model.value)
  form_data.append('user', user.value['id'])

  data.value = null
  show_loading_screen.value = true

  try {
    const token = JSON.parse(localStorage.getItem('token'))
    const response = await axios.post(
        'http://localhost:8000/api/submission/make_submission',
        form_data,
        { headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization' : 'Bearer ' + token['access']
        } }
    )
    localStorage.setItem('depressed', JSON.stringify(response.data['depressed']))
    localStorage.setItem('text', JSON.stringify(response.data['text']))

    // dodanie do historii predykcji ostatniego submission
    let previous_subs =  JSON.parse(localStorage.getItem('history_submissions'))
    previous_subs.unshift(response.data['submission'])
    localStorage.setItem('history_submissions', JSON.stringify(previous_subs))
    localStorage.setItem('choosen_submission', JSON.stringify(response.data['submission']))

    // aktualizacja danych usera
    user.value['submission_num'] -= 1
    localStorage.setItem('user', JSON.stringify(user.value))
    $cookies.set('made_submission', true)
    show_loading_screen.value = false
    await router.push('/predict')

  } catch (e) {
    handleErrorForSubmission(e)
  }
}

const makeSubmissionAnon = async () => {
  if (localStorage.hasOwnProperty('to_file')) {
    fromFileToData()
  } else if (!checkData()) {
    return
  }

  let form_data = new FormData()
  form_data.append('content', data.value)
  form_data.append('model', model.value)
  form_data.append('user', user.value['id'])

  data.value = null
  show_loading_screen.value = true

  try {
    const response = await axios.post(
        'http://localhost:8000/api/submission/make_submission',
        form_data,
        { headers: {
          'Content-Type': 'multipart/form-data'
        } }
    )
    localStorage.setItem('depressed', JSON.stringify(response.data['depressed']))
    localStorage.setItem('text', JSON.stringify(response.data['text']))

    $cookies.set('made_submission', true)
    show_loading_screen.value = false
    await router.push('/predict')

  } catch (e) {
    handleErrorForSubmission(e)
  }
}

watch(send_creator, () => {
  if (send_creator.value) {
    makePredictions()
  }
})

onMounted(() => {
  if (_.isEmpty(user.value)) {
    localStorage.setItem('choosen_model', JSON.stringify(model.value))
  } else {
    model.value = JSON.parse(localStorage.getItem('choosen_model'))
  }
})
</script>

<template>

  <ResponseOutput
      v-model:response_status="response_status"
      :after_create="after_create"
      v-if="response_status >= 200"
      :title="title"
      :subtitle="subtitle"
  ></ResponseOutput>

  <CreateFileOutput
      v-if="show_popup"
      v-model:show_popup="show_popup"
      v-model:send_creator="send_creator"
  ></CreateFileOutput>

  <div class="main" :style="{
    opacity: (show_loading_screen || show_popup || response_status > 200) ? '0.3' : '1',
    pointerEvents: (show_loading_screen || show_popup || response_status > 200) ? 'none' : 'auto'
  }">
    <div class="header">
      <span>Plik</span>
      <div class="choose" @click="choose = !choose" :style="{ justifyContent: !choose ? 'start' : 'end' }">
        <div
            class="circle"
            :style="{
              backgroundColor: choose ? 'mediumblue' : 'whitesmoke',
              borderColor: choose ? 'dodgerblue' : 'black'
            }"></div>
      </div>
      <span>Tekst</span>
    </div>
    <div class="depression-form" v-if="choose">
      <form @submit.prevent="makePredictions">

        <FormTextAreaField
            v-model:data="data"
        ></FormTextAreaField>

        <FormButtonField :login="true">
          <template v-slot:green>
            Zatwierdź
          </template>
        </FormButtonField>

      </form>
    </div>
    <div class="depression-form" v-else>
      <form @submit.prevent="makePredictions">

        <FormFileField
            v-model:is_dragging="is_dragging"
            v-model:data="data"
        ></FormFileField>

        <FormButtonField :login="true">
            <template v-slot:green>
              Zatwierdź
            </template>
          </FormButtonField>
      </form>
    </div>
 </div>
</template>

<style scoped>
.main {
  width: 100%;
  height: 80%;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
  gap: 1.5rem;
  margin: 1rem;
}

form {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
}

.header {
  width: 100%;
  height: 20%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}

.header > span {
  background-color: #ccc;
  border-radius: 1.5rem;
  padding: 1rem;
  font-weight: bold;
}

.choose {
  width: 15vw;
  height: 5vw;
  background-color: #ccc;
  border-radius: 2.5vw;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: background-color 0.3s ease;
  position: relative;
}

.choose:hover {
  background-color: #bbb;
}

.circle {
  width: 4vw;
  height: 4vw;
  background-color: whitesmoke;
  border-radius: 50%;
  border: 2px solid black;
  margin-left: 0.25rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.depression-form {
  width: 90%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
}

span {
  font-size: 1.5vw;
  color: #333;
}

@media (max-width: 700px) {
  form {
    flex-direction: column;
  }

  .main {
    font-size: 1.5vh;
  }

  .main * {
    font-size: 1.5vh !important;
  }

  .choose {
    width: 15vh;
    height: 5vh;
    border-radius: 2.5vh;
  }

  .circle.active {
    transform: translateX(10vh);
  }

  .circle {
    width: 4vh;
    height: 4vh;
  }
}

@media (max-height: 600px) {
  .main {
    font-size: 3vh;
  }

  .main * {
    font-size: 3vh !important;
  }

  .choose {
    width: 30vh;
    height: 10vh;
    border-radius: 5vh;
  }

  .circle.active {
    transform: translateX(20vh);
  }

  .circle {
    width: 8vh;
    height: 8vh;
  }
}
</style>