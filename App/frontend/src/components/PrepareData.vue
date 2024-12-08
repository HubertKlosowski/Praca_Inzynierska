<script setup>
import {inject, onMounted, ref, watch} from "vue";
import {useRouter} from "vue-router";
import axios from "axios";
import ResponseOutput from "@/components/ResponseOutput.vue";
import _ from "lodash";
import PopUp from "@/components/PopUp.vue";


const router = useRouter()
const $cookies = inject('$cookies')

const show_loading_screen = defineModel('show_loading_screen')
const show_popup = ref(JSON.parse(localStorage.getItem('show_popup')))
const send_creator = ref(false)
const user = ref(JSON.parse(localStorage.getItem('user')))
const choose = ref(true)
const data = ref(null)
const is_dragging = ref(false)
const models = ref(['roberta-base', 'bert-base'])

const after_create = ref({})
const title = ref('')
const subtitle = ref('')
const response_status = ref(0)


const makePredictions = async () => {
  let form_data = new FormData()
  show_popup.value = false

  if (localStorage.hasOwnProperty('to_file')) {
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
      title.value = 'Problem z podanymi danymi'
      subtitle.value = 'Proszę poprawić wprowadzone dane w kreatorze.'
    }
  } else {
    if (data.value === null) {
      after_create.value = ['Przekazane dane są puste!']
      response_status.value = 400
      title.value = 'Problem z podanymi danymi'
      subtitle.value = 'Modele nie są w stanie pracować na pustych danych. Proszę przesłać plik lub tekst.'
      return
    } else if (typeof data.value === 'object') {
      const extension = data.value.name.split('.')[1]
      if (extension !== 'csv' && extension !== 'json') {
        data.value = null
        after_create.value = ['Modele obsługują pliki z rozszerzeniem csv lub json.']
        response_status.value = 403
        title.value = 'Problem z podanymi danymi'
        subtitle.value = 'Nieprawidłowe rozszerzenie pliku. Proszę poprawić nazwę pliku i spróbować ponownie go przesłać.'
        return
      } else if (data.value.size > 10000 && _.isEmpty(user.value)) {
        data.value = null
        after_create.value = ['Limit wielkości pliku dla gościa wynosi 100KB.']
        response_status.value = 403
        title.value = 'Problem z podanymi danymi'
        subtitle.value = 'Zbyt duży plik. Proszę przesłać plik o mniejszej wielkości.'
        return
      }
    }
  }

  form_data.append('content', data.value)
  form_data.append('pl_model', models.value[0])
  form_data.append('en_model', models.value[1])

  if (!_.isEmpty(user.value)) {
    form_data.append('user', user.value['id'])
  }

  show_loading_screen.value = true

  localStorage.removeItem('to_file')

  try {
    const response = await axios.post('http://localhost:8000/api/submission/make_submission', form_data, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    localStorage.setItem('depressed', JSON.stringify(response.data['depressed']))
    localStorage.setItem('text', JSON.stringify(response.data['text']))

    if (!_.isEmpty(user.value)) {
      // dodanie do histori predykcji ostatniego submission
      let previous_subs =  JSON.parse(localStorage.getItem('history_submissions'))
      previous_subs.unshift(response.data['submission'])
      localStorage.setItem('history_submissions', JSON.stringify(previous_subs))
      localStorage.setItem('choosen_submission', JSON.stringify(response.data['submission']))

      // aktualizacja danych usera
      user.value['submission_num'] -= 1
      localStorage.setItem('user', JSON.stringify(user.value))
    }
    $cookies.set('made_submission', true)
    show_loading_screen.value = false
    await router.push('/predict')

  } catch (e) {
    show_loading_screen.value = false
    data.value = null

    if (typeof e.response === 'undefined' || e.status >= 500) {
      after_create.value = ['BŁĄD!! Nie udało się połączyć z serwerem.']
      response_status.value = 500
      title.value = 'Problem z serwerem'
      subtitle.value = 'Proszę poczekać, serwer nie jest teraz dostępny.'
    } else {
      const error_response = e.response
      after_create.value = error_response.data.error
      response_status.value = error_response.status
      title.value = 'Problem z podanymi danymi'
      subtitle.value = 'Przekazane dane zawierają błędy. Proszę się zapoznać z nimi i spróbować ponownie.'
    }
  }
}

const changeDragging = () => {
  is_dragging.value = !is_dragging.value
}

const drop = (event) => {
  changeDragging()
  data.value = event.dataTransfer.files[0]
}

const getFile = () => {
  data.value = document.getElementById('data').files[0]
}

watch(send_creator, () => {
  if (send_creator.value) {
    makePredictions()
  }
})

onMounted(() => {
  if (_.isEmpty(user.value)) {
    localStorage.setItem('choosen_models', JSON.stringify(models.value))
  } else {
    models.value = JSON.parse(localStorage.getItem('choosen_models'))
  }
})
</script>

<template>

  <ResponseOutput
      v-model:response_status="response_status"
      v-model:after_create="after_create"
      v-if="response_status >= 200"
      :title="title"
      :subtitle="subtitle"
  ></ResponseOutput>

  <PopUp
      v-if="show_popup"
      v-model:show_popup="show_popup"
      v-model:send_creator="send_creator"
  ></PopUp>

  <div class="main" :style="{
    opacity: (show_popup || response_status > 200) ? '0.3' : '1',
    pointerEvents: (show_popup || response_status > 200) ? 'none' : 'auto'
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
        <div class="form-row">
          <label for="data" class="text-label">Wpisz tekst do klasyfikacji depresji</label>
          <textarea id="data" v-model="data" placeholder="Tekst" class="form-textarea"></textarea>
          <button type="submit" class="confirm">Zatwierdź</button>
        </div>
      </form>
    </div>
    <div class="depression-form" v-else>
      <form @submit.prevent="makePredictions">
        <div class="form-row">
          <div
            @dragenter.prevent="changeDragging"
            @dragleave.prevent="changeDragging"
            @dragover.prevent
            @drop.prevent="drop"
            :class="{ 'drag-in': is_dragging, 'drag-out': !is_dragging }">
              <span>Upuść plik</span>
              <span>albo</span>
              <label for="data" class="file-label">Wybierz plik</label>
              <input type="file" id="data" @change="getFile" :style="{ display: 'none' }">
          </div>
          <button type="submit" class="confirm">Zatwierdź</button>
        </div>
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
  height: 100%;
  width: 100%;
  margin: 1rem;
}

.drag-in, .drag-out {
  height: 80%;
  border-radius: 0.75rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.7);
  text-align: center;
  align-content: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
}

.drag-in {
  background-color: gray;
  border: 3px dashed black;
}

.drag-out {
  background-color: lightgray;
  border: 3px solid black;
}

.header {
  width: 100%;
  height: 20%;
  display: flex;
  align-items: center;
  justify-content: space-evenly;
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
  width: 70%;
  height: 60%;
  margin: 0 auto;
  padding: 2rem;
  background-color: #f5f5f5;
  border-radius: 0.75rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
}

.form-row {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  height: 100%;
}

.text-label {
  font-size: 1.5vw;
  color: #333;
  font-weight: bold;
}

.file-label {
  padding: 0.5rem;
  border-radius: 1rem;
  border: 2px solid black;
  font-size: 1.35vw;
  background-color: lightgrey;
  transition: 0.4s ease;
}

.file-label:hover {
  color: white;
  border: 2px solid white;
  background-color: darkgrey;
  box-shadow: 1rem 1rem dodgerblue;
}

span {
  font-size: 1.5vw;
  color: #333;
}

.form-textarea {
  width: auto;
  height: 20%;
  min-height: 10%;
  max-height: 60%;
  padding: 0.75rem;
  font-size: 1.25vw;
  border: 1px solid #ccc;
  border-radius: 0.5rem;
  resize: vertical;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.form-textarea:focus {
  border-color: #4682B4;
  box-shadow: 0 0 5px rgba(70, 130, 180, 0.5);
  outline: none;
}

.confirm {
  padding: 0.75rem 1.5rem;
  font-size: 1.25vw;
  color: white;
  background-color: #4682B4;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.confirm:hover {
  background-color: #3a6a9b;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

@media (max-width: 768px) {
  .main {
    font-size: 1.5vh;
  }

  .main * {
    font-size: 1.5vh !important;
  }

  .choose {
    width: 15vh;
    height: 5vh;
  }

  .circle.active {
    transform: translateX(10vh);
  }

  .circle {
    width: 4vh;
    height: 4vh;
  }
}

@media (max-height: 550px) {
  .drag-in, .drag-out {
    display: flex;
    flex-direction: row;
    justify-content: space-evenly;
  }
}

@media (max-height: 650px) {
  .main {
    font-size: 3vh;
  }

  .main * {
    font-size: 3vh !important;
  }

  .choose {
    width: 30vh;
    height: 10vh;
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