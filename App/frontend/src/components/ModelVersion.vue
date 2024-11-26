<script setup>
import base from "@/assets/base.png";
import large from "@/assets/large.png";
import {inject} from "vue";

const $cookies = inject('$cookies')
const emits = defineEmits(['confirm'])

const setVersion = (param) => {
  emits('confirm', 2)
  $cookies.set('model_version', param)

  const activeElement = document.getElementsByClassName(param)[0]
  const inactiveElement = param === 'base'
      ? document.getElementsByClassName('large')[0]
      : document.getElementsByClassName('base')[0]

  activeElement.style.border = '2px solid black'
  activeElement.style.backgroundImage = `url(${
    param === 'base' ? base : large
  })`
  activeElement.style.backgroundRepeat = 'no-repeat'
  activeElement.style.backgroundSize = 'cover'
  activeElement.style.backgroundPosition = 'top'

  Array.from(activeElement.children).forEach(
    (child) => (child.style.display = 'none')
  )

  inactiveElement.style.border = 'none'
  inactiveElement.style.backgroundImage = 'none'

  Array.from(inactiveElement.children).forEach(
    (child) => (child.style.display = 'block')
  )
}
</script>

<template>
  <div class="main">
    <div class="base" @click="setVersion('base')">
      <h3>Wersja podstawowa</h3>
      <ul>
        <li>szybszy czas wykonania</li>
        <li>podstawowe zrozumienie danych tekstowych</li>
      </ul>
    </div>
    <div class="large" @click="setVersion('large')">
      <h3>Wersja rozszerzona</h3>
      <ul>
        <li>większą dokładność wyników.</li>
        <li>lepsze zrozumienie danych tekstowych</li>
        <li>3 razy większy o wersji podstawowej</li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.main {
  width: 100%;
  height: 80%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}

@media (max-width: 900px) {
  .main {
    flex-direction: column;
    font-size: 3vh;
  }

  .main * {
    font-size: 2vh !important;
  }

  .base, .large {
    width: 80% !important;
    height: 30% !important;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
  }
}

.base, .large {
  width: 40%;
  height: 80%;
  margin: 0 auto;
  background-color: #f5f5f5;
  border-radius: 0.75rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 1.5rem;
}

.base:hover, .large:hover {
  background-repeat: no-repeat;
  background-size: cover;
  background-position: top;
}

.base:hover {
  background-image: linear-gradient(rgba(255,255,255,0.5), rgba(255,255,255,0.5)), url("/src/assets/base.png");
}

.large:hover {
  background-image: linear-gradient(rgba(255,255,255,0.5), rgba(255,255,255,0.5)), url("/src/assets/large.png");
}
</style>