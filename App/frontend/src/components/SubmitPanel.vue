<script setup>
import { inject, ref } from 'vue'
import axios from 'axios'

const $cookies = inject('$cookies')

const llm_model = ref('')
const file = ref(null)
const show = ref(false)
const info = ref('')

const handleFile = (event) => {
  file.value = event.target.files[0]
}

const sendFile = async () => {
  let formData = new FormData()
  formData.append('file', file.value)
  formData.append('user', $cookies.get('user')['id'])
  formData.append('llm_model', llm_model.value)

  try {
    const response = await axios.post('http://localhost:8000/api/user/send_file', formData)
    info.value = response.data['success']
  } catch (error) {
    const error_response = error.response.data
    if (typeof error_response['error'] === 'string') {
      info.value = error_response['error']
    } else {
      info.value = error_response['error'].join(' ')
    }
  }
}
</script>

<template>
  <div class="submit" v-show="!show">
    <div class="form">
      <form @submit.prevent="sendFile">
        <h2>Wybierz model językowy</h2>
        <div class="radio_row">
          <div class="radio_item">
            <input type="radio" id="bert-base" value="bert-base" v-model="llm_model">
            <label for="bert-base">BERT-BASE</label>
          </div>
          <div class="radio_item">
            <input type="radio" id="bert-large" value="bert-large" v-model="llm_model">
            <label for="bert-large">BERT-LARGE</label>
          </div>
        </div>
        <label for="file">Wybierz plik</label>
        <input type="file" id="file" @change="handleFile"/>
        <button type="submit">Wyślij</button>
      </form>
    </div>
    <div class="info_icon" title="Informacje" @click="show = !show">
      &#x1F6C8;
    </div>
  </div>
  <div class="extra_info" v-show="show">
    <h2>Jak wykonać klasyfikację pliku?</h2>
    Wybierz jeden z podanych modeli językowych do klasyfikacji.<br>
    Podane modele są przetrenowane na danych w języku angielskim.<br>
    <ul>
      <li>Model BERT-BASE to podstawowa wersja, z około 110 milionów parametrów.</li>
      <li>Model BERT-LARGE natomiast posiada około 340 milionów parametrów.</li>
    </ul>
    Następnie podaj plik .csv, który spełnia wymagania podane na <a href="/details" target="_blank">stronie</a>.<br>
    Po wykonaniu tych czynności otrzymasz statystyki zbioru, który został przekazany.<br>
    😀😀😀😀😀
    <button type="button" id="return" @click="show = !show">Wróć</button>
  </div>
  <div
      class="info"
      :style="{ color: info.startsWith('BŁĄD') ? 'darkred' : 'darkgreen',
          display: info.length === 0 ? 'none' : 'initial' }"
  >
    {{ info }}
  </div>
</template>

<style scoped>
.submit, .extra_info {
  width: 90%;
  background-color: rgb(248, 249, 250);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  color: #2c3e50;
  display: flex;
  align-items: center;
  font-size: 1.2rem;
}

.submit {
  height: 90%;
  justify-content: space-between;
}

.extra_info {
  height: 70%;
  flex-direction: column;
  justify-content: space-evenly;
}

.info {
  width: 50%;
  margin: 10px;
  padding: 20px;
  background-color: rgb(248, 249, 250);
  border-radius: 8px;
  font-size: 1.2rem;
  text-align: center;
}

.form {
  width: 65%;
  height: 50%;
}

h2 {
  margin-bottom: 20px;
  font-size: 1.5rem;
  color: #2c3e50;
}

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 20px;
  background-color: powderblue;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.radio_row {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
}

.radio_item {
  display: flex;
  align-items: center;
}

.radio_item label {
  margin-left: 10px;
  font-size: 1rem;
  color: #2c3e50;
}

label {
  font-weight: bold;
  margin-bottom: 8px;
  color: #2c3e50;
}

input[type="radio"] {
  width: 1.2rem;
  height: 1.2rem;
  transform: translateY(-0.35em) translateX(0.35rem);
}

input[type="file"] {
  margin-top: 10px;
  padding: 8px;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  font-size: 1rem;
}

button[type="submit"] {
  padding: 10px;
  margin-top: 15px;
  background-color: #3498db;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button[type="submit"]:hover {
  background-color: #2980b9;
}

.info_icon {
  width: 25%;
  text-align: center;
  font-size: 4rem;
  color: #3498db;
  cursor: pointer;
}

.info_icon:hover {
  color: #2980b9;
}

#return {
  width: 10%;
  height: 10%;
  background-color: lightslategrey;
  text-decoration: none;
  text-align: center;
  font-size: 1.2rem;
  border-radius: 8px;
  padding: 10px 15px;
  color: white;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
}

#return:hover {
  background-color: darkslategrey;
}
</style>
