<script setup>
import {inject, onMounted, ref} from "vue";
import {useRouter} from "vue-router";
import axios from "axios";
import ResponseOutput from "@/components/ResponseOutput.vue";

const choose = ref(true)
const data = ref(null)
const is_dragging = ref(false)
const models = ref(['roberta-base', 'bert-base'])

const after_create = ref({})
const title = ref('')
const response_status = ref(0)
const show_loading_screen = defineModel('show_loading_screen')

const router = useRouter()
const $cookies = inject('$cookies')

const makePredictions = async () => {
  let form_data = new FormData()

  if (data.value === null) {
    after_create.value = ['BŁĄD!! Przekazane dane są puste!']
    response_status.value = 400
    title.value = 'Problem z podanymi danymi'
  } else if (typeof data.value === 'object') {
    const extension = data.value.name.split('.')[1]
    if (extension !== 'csv' && extension !== 'json') {
      console.log('BŁĄD!! Plik musi być w rozszerzeniu csv lub json.')
      data.value = null
    } else if (data.value.size > 150000 && !$cookies.isKey('user')) {
      console.log('BŁĄD!! Plik musi mniejszy od 150KB.')
      data.value = null
    }
    form_data.append('file', data.value)
  } else {
    form_data.append('entry', data.value)
  }

  form_data.append('pl_model', models.value[0])
  form_data.append('en_model', models.value[1])

  if ($cookies.isKey('user'))
    form_data.append('user', $cookies.get('user')['username'])

  show_loading_screen.value = true

  try {
    const response = await axios.post('http://localhost:8000/api/user/make_submission', form_data, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    localStorage.setItem('stats', JSON.stringify(response.data['stats']))
    localStorage.setItem('text', JSON.stringify(response.data['text']))

    if ($cookies.isKey('user') && $cookies.get('user')['id'] !== 0)
      localStorage.setItem('submission', JSON.stringify(response.data['submission']))

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
    } else {
      const error_response = e.response
      after_create.value = error_response.data.error
      response_status.value = error_response.status
      title.value = 'Problem z podanymi danymi'
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

onMounted(() => {
  if (!$cookies.isKey('user')) {
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
  ></ResponseOutput>

  <div class="main" :style="{
    opacity: response_status < 200 ? '1' : '0.3',
    pointerEvents: response_status < 200 ? 'auto' : 'none'
  }">
    <div class="header">
      <span>Plik</span>
      <div class="choose" @click="choose = !choose">
        <div :class="['circle', { active: choose }]"></div>
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
  border-radius: 1.5vw;
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
  transition: transform 0.3s ease, background-color 0.3s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.circle.active {
  transform: translateX(10vw);
  background-color: mediumblue;
  border-color: dodgerblue;
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