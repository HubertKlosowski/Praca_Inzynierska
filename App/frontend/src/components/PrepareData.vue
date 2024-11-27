<script setup>
import {inject, ref} from "vue";
import {useRouter} from "vue-router";
import axios from "axios";

const choose = ref(true)
const data = ref(null)
const is_dragging = ref(false)
const $cookies = inject('$cookies')

const router = useRouter()

const makePredictions = async () => {
  let form_data = new FormData()
  if (typeof data.value === 'object') {
    const extension = data.value.name.split('.')[1]
    if (extension !== 'csv' && extension !== 'json') {
      console.log('BŁĄD!! Plik musi być w rozszerzeniu csv lub json.')
      data.value = null
    } else if (data.value.size > 200000) {
      console.log('BŁĄD!! Plik musi mniejszy od 200KB.')
      data.value = null
    }
    form_data.append('file', data.value)
  } else {
    form_data.append('entry', data.value)
  }

  form_data.append('language', $cookies.get('model_language'))
  form_data.append('llm_model', $cookies.get('model') + '-' + $cookies.get('model_version'))
  form_data.append('user', 1)

  try {
    const response = await axios.post('http://localhost:8000/api/user/make_submission', form_data, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    localStorage.setItem('stats', JSON.stringify(response.data['stats']))
    localStorage.setItem('text', JSON.stringify(response.data['text']))
    localStorage.setItem('submission', JSON.stringify(response.data['submission']))

    $cookies.set('submission', true)

    await router.push('/predict')
  } catch (error) {

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
</script>

<template>
  <div class="main">
    <div class="header">
     <div class="choose" @click="choose = !choose">
       <div :class="['circle', { active: choose }]"></div>
     </div>
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
              <input type="file" id="data" @change="getFile" :style="{display: 'none'}">
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
  padding: 1rem;
}

@media (max-width: 768px) {
  .main {
    font-size: 1.5vh;
  }

  .main * {
    font-size: 1.5vh !important;
  }
}

form {
  height: 100%;
  width: auto;
  margin: 1rem;
}

.drag-in, .drag-out {
  width: auto;
  border-radius: 0.75rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.7);
  text-align: center;
  align-content: center;
}

.drag-in, .drag-out {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.drag-in > *, .drag-out > * {
  margin: 1%;
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
  justify-content: center;
}

.choose {
  width: 10rem;
  height: 3rem;
  background-color: #ccc;
  border-radius: 1.5rem;
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
  width: 2.5rem;
  height: 2.5rem;
  background-color: whitesmoke;
  border-radius: 50%;
  border: 2px solid black;
  margin-left: 0.25rem;
  transition: transform 0.3s ease, background-color 0.3s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.circle.active {
  transform: translateX(7rem);
  background-color: purple;
  border-color: purple;
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
  box-shadow: 1rem 1rem mediumpurple;
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
</style>