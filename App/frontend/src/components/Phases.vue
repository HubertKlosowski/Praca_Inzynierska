<script setup>
import Phase from "@/components/Phase.vue";
import {ref, watch} from "vue";

const global_num_phase = ref(0)
const phases_elements = document.getElementsByClassName('phase')

const phases = [
  {
    'title': 'Etap początkowy - konfiguracja modelu',
    'description': [
        'W tym etapie poznasz etapy, które należy przeprowadzić w konfiguracji.',
        'Na początku należy przygotować model.'
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
        'Wersja rozbudowana osiąga większą dokładność od wersji podstawowej.',
        'Wybierz pasującą dla Ciebie wersję.'
    ]
  },
  {
    'title': 'Twoja konfiguracja',
    'description': [
        'Konfiguracja modelu przebiegła prawidłowo.',
        'Jeszcze tylko dane ...'
    ]
  },
  {
    'title': 'Etap końcowy - przekaż dane',
    'description': [
        'Prześlij dane, na których chcesz przeprowadzić wykrywanie depresji.',
        'Istnieją dwa możliwe sposoby przekazania danych: z pliku lub jako pojedyńczy tekst.'
    ]
  },
]

watch(global_num_phase, (newValue, oldValue) => {
  phases_elements[oldValue].style.backgroundColor = '#E0E0E0'
  phases_elements[newValue].style.backgroundColor = 'red'
})
</script>

<template>
  <div class="left-part">
    <div class="phases">
      <div class="phase" v-for="i in 5" :key="i"></div>
    </div>
    <Phase
        v-if="phases[global_num_phase]"
        :phase="phases[global_num_phase]"
        :num_phase="global_num_phase"
        @nextOne="(next_num_phase) => {
          global_num_phase = next_num_phase
        }"
        @previousOne="(next_num_phase) => {
          global_num_phase = next_num_phase
        }
    ">

    </Phase>
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
</style>