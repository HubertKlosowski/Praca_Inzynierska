<script setup>
import Phase from "@/components/Phase.vue";
import {ref, watch} from "vue";

const global_num_phase = ref(0)
const phases_elements = document.getElementsByClassName('phase')

const phases = [
  {
    'title': 'Przekaż dane',
    'description': [
        'Prześlij dane, na których chcesz przeprowadzić wykrywanie depresji.',
        'Istnieją dwa możliwe sposoby przekazania danych: z pliku lub jako pojedyńczy tekst.'
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
    <Phase
        v-if="phases[global_num_phase]"
        :phase="phases[global_num_phase]"
        v-model:global_num_phase="global_num_phase"
    >

    </Phase>
  </div>
</template>

<style scoped>
.left-part {
  width: 90%;
}

.phase:first-child {
  background-color: red;
}

@media (max-height: 500px) {
  .phase {
    height: 20px;
    width: 20px;
  }
}
</style>