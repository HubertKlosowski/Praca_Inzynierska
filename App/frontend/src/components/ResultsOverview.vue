<script setup>
import {inject} from "vue";

const $cookies = inject('$cookies')

const hardToAccess = () => {
  const results = $cookies.get('stats')['depressed']
  let res = 0

  for (let i = 0; i < results.length; i++) {
    if (results[i] > 0.45 && results[i] < 0.55) {
      res += 1
    }
  }
  return res
}
</script>

<template>
<div class="general-info">
  <div class="general">
    <div class="info">
      Czas wykonania (s): {{ $cookies.get('submission')['time_taken'].toFixed(2) }}
    </div>
    <div class="info">
      Liczba rekordów: {{ $cookies.get('text').length }}
    </div>
    <div class="info">
      Liczba "trudnych" rekordów : {{ hardToAccess() }}
    </div>
    <div class="info">
      Użytkownik: {{ $cookies.get('submission')['user'] }}
    </div>
    <div class="info">
      Nazwa modelu: {{ $cookies.get('submission')['llm_model'] }}
    </div>
  </div>
  <div class="avg-semi-circle">

  </div>
</div>
</template>

<style scoped>
@media (max-width: 768px) {
  .general-info {
    flex-direction: column;
    font-size: 1.2vh !important;
  }
}

.info {
  width: auto;
  height: 20%;
  background-color: lightgray;
  margin: 1rem;
  padding: 1rem;
  border-radius: 0.75rem;
}

.general {
  overflow-y: auto;
}

.general, .avg-semi-circle {
  width: 45%;
  height: 90%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 1rem;
  padding: 1rem 0 1rem 0;
  border-radius: 0.75rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.7);
  background-color: #f5f5f5;
}

.general-info {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}
</style>