<script setup>
import {inject, onMounted, ref} from "vue";

const $cookies = inject('$cookies')
const show = ref(false)

const generateProgressBar = () => {
  const results = $cookies.get('stats')['depressed']
  const bars = document.querySelectorAll('.bar')

  for (let i = 0; i < bars.length; i++) {
    bars[i].style.width = results[i] * 100 + '%'
  }
}

onMounted(() => {
  generateProgressBar()
})
</script>

<template>
  <div class="predictions">
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
   <div class="row" v-for="(item, index) in $cookies.get('text')" :key="index">
     <div class="text" :style="{width: show ? '20%' : '80%', opacity: show ? '0.3' : '1'}">
       {{ item }}
     </div>
     <div class="propability" :style="{width: !show ? '20%' : '80%', opacity: !show ? '0.3' : '1'}">
       <div class="progress" :style="{
         color: ($cookies.get('stats')['depressed'][index] * 100).toFixed(2) >= 25 ? 'white' : 'black',
         textAlign: 'center'
       }">
         {{ ($cookies.get('stats')['depressed'][index] * 100).toFixed(2) }}
         <div class="bar"></div>
       </div>
     </div>
   </div>
  </div>
</template>

<style scoped>
@media (max-width: 768px) {
  .text {
    font-size: 1.5vh !important;
  }
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
  position: relative;
  width: 90%;
  height: 50%;
  border: 2px solid black;
  margin-right: 0.5rem;
  z-index: 1;
}

.text {
  overflow-x: auto;
  padding: 1rem;
  font-size: 1.2vw;
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
</style>