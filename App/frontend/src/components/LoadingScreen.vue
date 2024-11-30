<script setup>
import {ref, watch} from "vue";

const text = ref([
  'Proszę czekać, model generuje wyniki.',
  'Nie ignoruj objawów depresji.',
  'Potrzebujesz pomocy?',
  'Infolinia wsparcia psychicznego: 800 70 2222.',
  'Szukanie pomocy to nie wstyd, dbaj o swoje zdrowie.'
])
const index = ref(0)

watch(index, () => {
  setTimeout(() => {
    if (index.value === text.value.length - 1) {
      index.value = 0
    } else {
      index.value += 1
    }
  }, 2000)
}, { immediate: true })
</script>

<template>
  <div class="load">
    <div class="circle"></div>
    <div class="text">
      {{ text[index] }}
    </div>
  </div>
</template>

<style scoped>
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.load {
  position: fixed;
  top: 0;
  right: 0;
  left: 0;
  bottom: 0;
  width: auto;
  height: 100%;
  padding: 2rem;
  background-color: rgba(245, 245, 245, 0.95);
  border-radius: 1rem;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  color: #333;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
}

.circle {
  width: 10vw;
  height: 10vw;
  border: 2vw solid lightgray;
  border-top: 2vw solid #3498db;
  border-bottom: 2vw solid #3498db;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.95);
  animation: spin 3s ease-in-out infinite;
}

.text {
  width: 100%;
  height: 20%;
  background-color: #f5f5f5;
  font-size: 2vw;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  border-radius: 0.75rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.7);
  padding: 1rem;
}

@media (max-width: 768px) {
  .text {
    font-size: 1.5vh;
  }

  .circle {
    width: 10vh;
    height: 10vh;
    border: 2vh solid lightgray;
    border-top: 2vh solid #3498db;
    border-bottom: 2vh solid #3498db;
  }
}
</style>