<script setup>
import {ref} from "vue";
import Results from "@/components/Results.vue";
import ResultsPlot from "@/components/ResultsPlot.vue";
import ResultsOverview from "@/components/ResultsOverview.vue";
import {useRouter} from "vue-router";
import _ from "lodash";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";


const router = useRouter()

const inc = ref(0)
const size = ref(JSON.parse(localStorage.getItem('text')).length)
const user = ref(JSON.parse(localStorage.getItem('user')))
const response_status = ref(0)


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

const goHome = async () => {
  await router.push('/')
}
</script>

<template>
 <div class="left-part">
   <div class="main">

     <Results v-if="inc === 0"></Results>

     <ResultsOverview v-if="inc === 1" v-model:response_status="response_status"></ResultsOverview>

     <ResultsPlot v-if="inc === 2"></ResultsPlot>

   </div>
   <div class="buttons">
     <div class="move" @click="changeSection(-1)" :style="{
       display: !_.isEmpty(user) ? 'initial' : 'none',
       opacity: response_status === 0 ? '1' : '0.3',
       pointerEvents: response_status === 0 ? 'auto' : 'none'
     }">
      <font-awesome-icon :icon="['fas', 'circle-arrow-left']" />
     </div>
     <div class="move" :style="{
       width: '30%',
       opacity: response_status === 0 ? '1' : '0.3',
       pointerEvents: response_status === 0 ? 'auto' : 'none'
     }">
       <font-awesome-icon :icon="['fas', 'house']" class="router-link" @click="goHome" />
     </div>
     <div class="move" @click="changeSection(1)" :style="{
       display: !_.isEmpty(user) ? 'initial' : 'none',
       opacity: response_status === 0 ? '1' : '0.3',
       pointerEvents: response_status === 0 ? 'auto' : 'none'
     }">
      <font-awesome-icon :icon="['fas', 'circle-arrow-right']" />
     </div>
   </div>
 </div>
</template>

<style scoped>
.router-link {
  width: 20%;
  height: 50%;
  padding: 1rem;
}

svg {
  width: 100%;
  height: 100%;
}

.move {
  width: 15%;
  height: 50%;
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
  overflow-y: hidden;
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

@media (max-width: 700px) {
  .left-part {
    flex-direction: column;
    font-size: 1.5vh !important;
  }
}
</style>