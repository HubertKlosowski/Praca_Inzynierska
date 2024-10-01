<script setup>
import { inject, ref } from 'vue'
import axios from 'axios'
import PolishSubmitFile from '@/components/SubmitPolishFile.vue'
import EnglishSubmitFile from '@/components/SubmitEnglishFile.vue'
import english from '@/assets/angielski.png'
import polish from '@/assets/polski.png'

const $cookies = inject('$cookies')

const change_lang = ref(true)
const show = ref(false)
const info = ref('')

const predict = async (llm_model, file) => {
  let formData = new FormData()
  formData.append('file', file)
  formData.append('user', $cookies.get('user')['id'])
  formData.append('llm_model', llm_model)

  if (file === null || llm_model.length === 0) {
    info.value = 'BŁĄD!! Nie można wysłać pustych danych formularza.'
  } else {
    try {
      info.value = 'Proszę poczekać, przeprowadzane są obliczenia!!'
      const response = await axios.post('http://localhost:8000/api/user/send_file', formData)
      info.value = response.data['success']
      $cookies.set('confusion_matrix', response.data['stats']['confusion_matrix'])
      $cookies.set('metrics', response.data['stats']['metrics'])
    } catch (error) {
      const error_response = error.response.data
      if (typeof error_response['error'] === 'string') {
        info.value = error_response['error']
      } else if (typeof error_response['error'] === 'undefined') {
        info.value = 'BŁĄD!! Nie udało się połączyć z serwerem.'
      } else {
        info.value = error_response['error'].join(' ')
      }
    }
  }
}
</script>

<template>
  <div class="submit" v-if="!show">
    <div class="change_lang">
      <div
          class="circle"
          @click="change_lang = !change_lang"
          :style="{
            background: change_lang ? `url(${english}) center` : `url(${polish}) center`,
            backgroundSize: '100% 100%',
            transform: change_lang ? 'translate(50%)' : 'translate(-50%)'
             }"
      ></div>
    </div>
    <div class="content" v-if="change_lang">
      <EnglishSubmitFile
          @send-data="([eng_llm_model, eng_file]) => { predict(eng_llm_model, eng_file) }"
      ></EnglishSubmitFile>
      <div class="info_icon" title="Informacje" @click="show = !show">
        &#x1F6C8;
      </div>
    </div>
    <div class="content" v-else>
      <PolishSubmitFile
          @send-data="([pl_llm_model, pl_file]) => { predict(pl_llm_model, pl_file) }"
      ></PolishSubmitFile>
      <div class="info_icon" title="Informacje" @click="show = !show">
        &#x1F6C8;
      </div>
    </div>
  </div>
  <div class="extra_info" v-else>
    <h2>Jak wykonać klasyfikację pliku?</h2>
    Na początku wybierz w jakim języku są twoje dane.<br>
    W zależności od języka pojawią się modele specjalnie do nich przeznaczone<br>
    Wybierz jeden z podanych modeli językowych do klasyfikacji.<br>
    <ol>
      <li>dla języka angielskiego
        <ol>
          <li>Model BERT-BASE to podstawowa wersja, z około 110 milionów parametrów.</li>
          <li>Model BERT-LARGE natomiast posiada około 340 milionów parametrów.</li>
        </ol>
      </li>
      <li>dla języka polskiego
        <ol>
          <li>Model RoBERTa-BASE</li>
          <li>Model RoBERTa-LARGE</li>
        </ol>
      </li>
    </ol>
    Następnie podaj plik .csv, który spełnia wymagania podane na <a href="/details" target="_blank">stronie</a>.<br>
    Po wykonaniu tych czynności otrzymasz statystyki zbioru, który został przekazany.<br>
    😀😀😀😀😀
    <button type="button" id="return" @click="show = !show">Wróć</button>
  </div>
  <div
      class="info"
      :style="{
    color: info.startsWith('BŁĄD') ? 'darkred' : 'darkgreen',
    display: info.length === 0 ? 'none' : 'initial' }"
  >
    {{ info }}
  </div>
</template>

<style scoped>
.change_lang {
  width: 15%;
  height: 20%;
  background-color: lightgrey;
  border-radius: 35%;
  border: 2px solid black;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
}

.circle {
  width: 35%;
  height: 70%;
  border-radius: 100%;
}

.content {
  width: 100%;
  height: 100%;
  padding: 20px;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
}

.submit, .extra_info {
  width: 90%;
  height: 100vh;
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
  flex-direction: column;
  justify-content: space-between;
}

.extra_info {
  flex-direction: column;
  justify-content: space-evenly;
  overflow-y: auto;
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

ol, li {
  padding: 5px;
}
</style>
