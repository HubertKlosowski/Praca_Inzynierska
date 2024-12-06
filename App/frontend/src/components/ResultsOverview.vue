<script setup>
import _ from "lodash";
import {ref} from "vue";


const stats = ref(JSON.parse(localStorage.getItem('depressed')))
const text = ref(JSON.parse(localStorage.getItem('text')))
const submission = ref(JSON.parse(localStorage.getItem('choosen_submission')))
const user = ref(JSON.parse(localStorage.getItem('user')))


const hardToAccess = () => {
  let res = _.filter(stats, function (num) {
    return num > 0.45 && num < 0.55
  })
  return _.size(res)
}
</script>

<template>
  <div class="general-info">
    <div class="info">
      Czas wykonania (s): {{ submission['time_taken'].toFixed(2) }}
    </div>
    <div class="info" v-if="text.length > 1">
      Liczba rekordów: {{ text.length }}
    </div>
    <div class="info" v-else>
      Pojedyńczy wpis
    </div>
    <div class="info" v-if="text.length > 1">
      Liczba "trudnych" rekordów : {{ hardToAccess() }}
    </div>
    <div class="info" v-else>
      Brak "trudnych" rekordów
    </div>
    <div class="info">
      Użytkownik: {{ user['username'] }}
    </div>
    <div class="info">
      Nazwa modelu: {{ submission['model'] }}
    </div>
  </div>
</template>

<style scoped>
.info {
  width: 70%;
  height: 10%;
  background-color: lightgray;
  border-radius: 0.75rem;
  text-align: center;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  padding: 1rem;
}

.general-info {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
}
</style>