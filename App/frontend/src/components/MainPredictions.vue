<script setup>
import {ref} from "vue";
import Results from "@/components/Results.vue";
import ResultsPlot from "@/components/ResultsPlot.vue";
import ResultsOverview from "@/components/ResultsOverview.vue";

const inc = ref(0)
const size = ref(JSON.parse(localStorage.getItem('text')).length)
const user = ref(JSON.parse(localStorage.getItem('user')))

const changeSection = (param) => {
  let limit_up
  const limit_down = 0

  if (user.value['usertype'] >= 1 && size.value > 1) {
    limit_up = 2
  } else {
    limit_up = 1
  }

  if (inc.value === limit_up && param === 1) {
    inc.value = 0
  } else if (inc.value === limit_down && param === -1) {
    inc.value = limit_up
  } else {
    inc.value += param
  }
}
</script>

<template>
 <div class="left-part">
   <div class="main">

     <Results v-if="inc === 0"></Results>

     <ResultsOverview v-if="inc === 1"></ResultsOverview>

     <ResultsPlot v-if="inc === 2"></ResultsPlot>

   </div>
   <div class="buttons">
     <div class="move" @click="changeSection(-1)" :style="{
       display: user !== null ? 'initial' : 'none'
     }">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
        <path d="M512 256A256 256 0 1 0 0 256a256 256 0 1 0 512 0zM215 127c9.4-9.4 24.6-9.4 33.9 0s9.4 24.6 0 33.9l-71 71L392 232c13.3 0 24 10.7 24 24s-10.7 24-24 24l-214.1 0 71 71c9.4 9.4 9.4 24.6 0 33.9s-24.6 9.4-33.9 0L103 273c-9.4-9.4-9.4-24.6 0-33.9L215 127z"/>
      </svg>
     </div>
     <RouterLink to="/" class="router-link">Wróć do strony głównej</RouterLink>
     <div class="move" @click="changeSection(1)" :style="{
       display: user !== null ? 'initial' : 'none'
     }">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
        <path d="M0 256a256 256 0 1 0 512 0A256 256 0 1 0 0 256zM297 385c-9.4 9.4-24.6 9.4-33.9 0s-9.4-24.6 0-33.9l71-71L120 280c-13.3 0-24-10.7-24-24s10.7-24 24-24l214.1 0-71-71c-9.4-9.4-9.4-24.6 0-33.9s24.6-9.4 33.9 0L409 239c9.4 9.4 9.4 24.6 0 33.9L297 385z"/>
      </svg>
     </div>
    </div>
 </div>
</template>

<style scoped>
.move {
  width: 15%;
  height: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}

.main {
  width: 100%;
  height: 80%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-bottom: 1rem;
}

.left-part {
  width: 90%;
}

.buttons {
  border-top: 2px solid black;
  width: 100%;
  height: 20%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}

@media (max-width: 768px) {
  .left-part {
    flex-direction: column;
    font-size: 1.5vh !important;
  }

  svg {
    width: 5vw;
    height: auto;
  }
}

@media (max-height: 950px) {
  svg {
    width: 15vh;
    height: auto;
  }
}
</style>