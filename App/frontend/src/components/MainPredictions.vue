<script setup>
import {inject, onMounted, ref} from "vue";

const inc = ref(1)
const show = ref(false)
const $cookies = inject('$cookies')

const generateProgressBar = () => {
  const results = $cookies.get('submission')['stats']['depressed']
  const progress_bars = document.getElementsByClassName('bar')
  for (let i = 0; i < progress_bars.length; i++) {
    progress_bars[i].style.width = results[i] * 100 + '%'
  }
}

const changeSection = (param) => {
  if (inc.value === 3 && param === -1) {
    inc.value = 1
  } else if (inc.value === 1 && param === 1) {
    inc.value = 3
  } else {
    inc.value -= param
  }
}

onMounted(() => {
  generateProgressBar()
})
</script>

<template>
 <div class="left-part">
   <div class="main">
     <div class="content">
       <div class="predictions" v-if="inc === 1">
         <div class="header">
           <div class="title-text" :style="{width: show ? '20%' : '80%'}">
             <div
               class="different-sizes"
               @click="show = !show"
               :style="{backgroundColor: !show ? 'green' : 'red'}"
             >

             </div>
             <span>Wpis</span>
           </div>
           <div class="title-proba" :style="{width: !show ? '20%' : '80%'}">
             <span>Stopień depresji</span>
           </div>
         </div>
         <div class="row" v-for="(item, index) in $cookies.get('submission')['text']" :key="index">
           <div class="text" :style="{width: show ? '20%' : '80%', opacity: show ? '0.3' : '1'}">
             {{ item }}
           </div>
           <div class="propability" :style="{width: !show ? '20%' : '80%', opacity: !show ? '0.3' : '1'}">
             <div class="progress">
               <div class="bar"></div>
             </div>
           </div>
         </div>
       </div>

       <div class="general-info" v-if="inc === 2">

       </div>
       <div class="plot" v-if="inc === 3">

       </div>
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

  .text {
    font-size: 1.5vh !important;
  }
}

.bar {
  width: 0;
  height: 100%;
  margin: 0 1rem 0 0;
  background-color: red;
}

.title-text, .title-proba {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
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

.different-sizes {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background-color: #007BFF;
  cursor: pointer;
  transition: transform 0.3s ease-in-out, background-color 0.3s ease-in-out;
}

.different-sizes:hover {
  transform: scale(1.2);
}

.header {
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
  width: 90%;
  height: 50%;
  border: 2px solid black;
  margin-right: 0.5rem;
}

.text {
  overflow-x: auto;
  padding: 1rem;
  font-size: 1.2vw;
}

.emotion {
  width: 50px;
  height: 50px;
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
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
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