<script setup>
import ModelPhase from "@/components/ModelPhase.vue";
import {ref, watch} from "vue";

const global_num_phase = ref(0)
const phases_elements = document.getElementsByClassName('phase')

const phases = [
  {
    'title': 'Wstęp',
    'description': [
        'Dane zostały wprowadzone oraz przesłane poprawnie.',
        'Czas na wybór modelu do wskazania depresji.'
    ]
  },
  {
    'title': 'Dobór modelu do języka danych',
    'description': [
        'Różne modele pasują do różnych języków.',
        'Wybierz model, który obsługuję język występujący w twoich danych.'
    ]
  },
  {
    'title': 'Wersja modelu',
    'description': [
        'Wersja BASE jest szybsza od LARGE, natomiast model LARGE zwróci lepsze wyniki.',
        'Wybierz pasującą dla Ciebie wersję.'
    ]
  },
  {
    'title': 'Zatwierdź',
    'description': [
        'Konfiguracja modelu przebiegła prawidłowo.',
        'Model pracuje nad predykcjami',
        'Proszę czekać, to może potrwać chwilę ...'
    ]
  }
]

watch(global_num_phase, (newValue, oldValue) => {
  phases_elements[oldValue].style.backgroundColor = '#E0E0E0'
  phases_elements[newValue].style.backgroundColor = 'red'
})
</script>

<template>
  <div class="left-part">
    <div class="phases">
      <div class="phase" v-for="i in 4" :key="i"></div>
    </div>
    <ModelPhase
        v-if="phases[global_num_phase]"
        :phase="phases[global_num_phase]"
        :num_phase="global_num_phase"
        @nextOne="(next_num_phase) => {
          global_num_phase = next_num_phase
        }"
        @previousOne="(next_num_phase) => {
          global_num_phase = next_num_phase
        }"></ModelPhase>
    <div class="buttons" v-if="global_num_phase === 3">
      <RouterLink to="/data" class="router-link">Wróć</RouterLink>
      <RouterLink to="/predict" class="router-link">Dalej</RouterLink>
    </div>
  </div>
</template>

<style scoped>
.left-part {
  width: 90%;
}

.phase {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #E0E0E0;
  transition: background-color 0.3s ease;
}

.phases {
  height: 10%;
  width: 100%;
  margin: 0 0 3% 0;
  background-color: #f5f5f5;
  border-radius: 0.75rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}

.phase:first-child {
  background-color: red;
}

.buttons {
  width: 100%;
  height: 15%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}
</style>