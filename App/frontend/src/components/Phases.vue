<script setup>
import Phase from "@/components/Phase.vue";
import {ref} from "vue";

const global_num_phase = ref(0)

const phases = [
  {
    'title': 'Przekaż dane',
    'description': [
        'Prześlij dane, na których chcesz przeprowadzić wykrywanie depresji.',
        'Istnieją dwa możliwe sposoby przekazania danych: jako pojedynczy tekst albo w postaci pliku.'
    ]
  }
]
</script>

<template>
  <div class="left-part">
    <Phase
        v-if="phases[global_num_phase]"
        :phase="phases[global_num_phase]"
        v-model:global_num_phase="global_num_phase"
    ></Phase>
  </div>
</template>

<style scoped>
.left-part {
  width: 90%;
}
</style>