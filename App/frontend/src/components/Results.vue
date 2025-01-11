<script setup>
import {onMounted, ref} from "vue";
import _ from "lodash";


const show = ref(false)
const sort = ref(0)
const text = ref(JSON.parse(localStorage.getItem('text')))
const stats = ref(JSON.parse(localStorage.getItem('depressed')))


const generateProgressBar = () => {
  const bars = document.querySelectorAll('.bar')

  for (let i = 0; i < bars.length; i++) {
    if (stats.value[i] !== -1)
      bars[i].style.width = stats.value[i] * 100 + '%'
  }
}

const sortByValue = () => {
  let concated = _.zip(text.value, stats.value)  // łączenie po kolumnach

  if (sort.value === 0) {
    concated = _.orderBy(concated, (row) => row[1], ['asc'])  // sortowanie po wartości depresji rosnąco
  } else if (sort.value === 1) {
    concated = _.orderBy(concated, (row) => row[1], ['desc'])
  } else {
    concated = _.zip(JSON.parse(localStorage.getItem('text')), JSON.parse(localStorage.getItem('depressed')))
  }

  concated = _.unzip(concated)
  text.value = concated[0]
  stats.value = concated[1]

  generateProgressBar()

  sort.value += 1
  if (sort.value === 3) {
    sort.value = 0
  }
}

onMounted(() => {
  generateProgressBar()
})
</script>

<template>
  <div class="header">
   <div class="title-text" :style="{ width: show ? '20%' : '80%' }">
     <div
       class="different-sizes"
       @click="show = !show"
       :style="{ backgroundColor: !show ? 'green' : 'red' }"
     >

     </div>
     <span>Wpis</span>
   </div>
   <div class="title-proba" :style="{width: !show ? '20%' : '80%'}">
     <div class="move" :style="{ display: show ? 'flex' : 'none' }" v-if="sort === 0" @click="sortByValue">
       <font-awesome-icon :icon="['fas', 'circle-arrow-up']" />
     </div>
     <div class="move" :style="{ display: show ? 'flex' : 'none' }" v-if="sort === 1" @click="sortByValue">
       <font-awesome-icon :icon="['fas', 'circle-arrow-down']" />
     </div>
     <div class="move" :style="{ display: show ? 'flex' : 'none' }" v-if="sort === 2" @click="sortByValue">
       <font-awesome-icon :icon="['fas', 'arrow-down-up-across-line']" />
     </div>
     <span>Stopień depresji</span>
   </div>
  </div>
  <div class="predictions">
   <div class="row" v-for="(item, index) in text" :key="index">
     <div class="text" :style="{
       width: show ? '20%' : '80%',
       opacity: show ? '0.3' : '1'
     }">
       {{ item }}
     </div>
     <div
         class="propability"
         :style="{
           width: !show ? '20%' : '80%',
           opacity: !show ? '0.3' : '1'
         }">
       <div
           class="progress"
           v-if="stats[index] !== -1"
           :style="{
             color: (stats[index] * 100).toFixed(2) >= 50 ? 'white' : 'black',
             textAlign: 'center'
           } ">
         {{ (stats[index] * 100).toFixed(2) }}
         <div class="bar"></div>
       </div>
       <div class="progress" v-else style="border: none;">
         Wpis zbyt długi do oceny.
         <div class="bar" style="display: none"></div>
       </div>
     </div>
   </div>
  </div>
</template>

<style scoped>
svg {
  width: 100%;
  height: auto;
}

.bar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: -1;
  height: 100%;
  background-color: black;
  margin-right: 1rem;
}

.title-text, .title-proba {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: start;
  gap: 1rem;
  padding: 0 2rem 0 2rem;
}

.header:nth-child(2) {
  border-left: 2px solid black;
}

.title-text, .title-proba, .propability, .text {
  width: 50%;
  height: 50px;
  transition: all 0.3s ease-in-out;
}

.move {
  width: 30px;
  height: auto;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}

.different-sizes {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  cursor: pointer;
  transition: transform 0.3s ease-in-out, background-color 0.3s ease-in-out;
}

.different-sizes:hover {
  transform: scale(1.2);
}

.header {
  width: 100%;
  height: 50px;
  margin: 1rem;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  text-align: center;
  background-color: gray;
}

.propability {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.progress {
  position: relative;
  width: 90%;
  height: 50%;
  border: 2px solid black;
  margin-right: 0.5rem;
  z-index: 1;
}

.text {
  overflow: hidden;
  padding: 1rem;
  font-size: 1.5vw;
}

.text:hover {
  overflow-y: visible;
}

.row {
  height: 50px;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
  margin: 1rem;
  padding: 1rem 0 1rem 0;
  border-radius: 0.75rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.7);
  background-color: #f5f5f5;
}

.predictions {
  width: 100%;
  height: 80%;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

@media (max-width: 700px) {
  .text {
    font-size: 1.5vh !important;
  }

  .progress {
    font-size: 1.5vh !important;
  }
}
</style>