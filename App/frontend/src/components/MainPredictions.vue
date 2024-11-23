<script setup>
import {inject, ref} from "vue";
import Results from "@/components/Results.vue";
import ResultsPlot from "@/components/ResultsPlot.vue";
import ResultsOverview from "@/components/ResultsOverview.vue";

const inc = ref(1)
const $cookies = inject('$cookies')

const changeSection = (param) => {
  const limit_up = $cookies.get('submission')['file'] !== null ? 3 : 2
  if (inc.value === limit_up && param === -1) {
    inc.value = 1
  } else if (inc.value === 1 && param === 1) {
    inc.value = $cookies.get('submission')['file'] !== null ? 3 : 2
  } else {
    inc.value -= param
  }
}
</script>

<template>
 <div class="left-part">
   <div class="main">
     <div class="content">

       <Results v-if="inc === 1"></Results>

       <ResultsOverview v-if="inc === 2"></ResultsOverview>

       <ResultsPlot v-if="inc === 3 && $cookies.get('submission')['file'] !== null"></ResultsPlot>

     </div>
   </div>
   <div class="buttons">
     <div class="go-back" @click="changeSection(-1)">
      <svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" fill="currentColor" class="bi bi-arrow-left-circle" viewBox="0 0 16 16">
        <path fill-rule="evenodd" d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8m15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-4.5-.5a.5.5 0 0 1 0 1H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5z"/>
      </svg>
     </div>
     <RouterLink to="/" class="router-link">Powrót do strony głównej</RouterLink>
     <div class="go-next" @click="changeSection(1)">
      <svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" fill="currentColor" class="bi bi-arrow-left-circle" viewBox="0 0 16 16">
        <path fill-rule="evenodd" d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8m15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0M4.5 7.5a.5.5 0 0 0 0 1h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5z"/>
      </svg>
     </div>
    </div>
 </div>
</template>

<style scoped>
@media (max-width: 768px) {
  .left-part {
    flex-direction: column;
    font-size: 1.5vh !important;
  }
}

.content {
  width: 100%;
  height: 100%;
}

.go-back, .go-next {
  width: 15%;
  height: auto;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}

.main {
  width: 100%;
  height: 70%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  margin-bottom: 1rem;
}

.left-part {
  width: 90%;
}

.buttons {
  width: 100%;
  height: 20%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}
</style>