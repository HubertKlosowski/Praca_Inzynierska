<script setup>
import polish from "@/assets/polski.png";
import english from "@/assets/angielski.png";
import {inject} from "vue";

const $cookies = inject('$cookies')
const emits = defineEmits(['confirm'])

const setLanguage = (param) => {
  emits('confirm', 1)
  $cookies.set('model_language', param)
  param === 'pl' ? $cookies.set('model', 'roberta') : $cookies.set('model', 'bert')

  const activeElement = param === 'pl'
      ? document.getElementsByClassName('polish')[0]
      : document.getElementsByClassName('english')[0]
  const inactiveElement = param === 'pl'
      ? document.getElementsByClassName('english')[0]
      : document.getElementsByClassName('polish')[0]

  activeElement.style.border = '2px solid black'
  activeElement.style.backgroundImage = `url(${
    param === 'pl' ? polish : english
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
    <div class="polish" @click="setLanguage('pl')">
      <p>
        Wszystkie języki różnią się od siebie.
        Gramatyka, słownictwo, sposób zapisu zdań ma gigantyczny wpływ na wskazanie emocji w tekście.
      </p>
      <p>
        Modele podobnie jak my ludzie muszą się nauczyć języka aby móc go "rozumieć".
        Jeśli nauczą się jednego języka, np. polskiego nie są w stanie bez wcześniejszego przygotowania rozumieć słów w innym języku.
      </p>
    </div>
    <div class="english" @click="setLanguage('en')">
      <p>
        Nieprawidłowo wybrany język może spowodować otrzymanie błędnych wyników w predykcjach.
        Dlatego tak ważnym jest wybranie modelu pod języku przekazanych danych.
      </p>
      <p style="font-weight: bold">
        Kliknij w jeden z tych przycisków aby wybrać język polski (po lewej) albo język angielski (po prawej).
      </p>
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
    font-size: 1.5vh;
  }

  .main * {
    font-size: 1.5vh !important;
  }

  .polish, .english {
    width: 80% !important;
    height: 30% !important;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
  }
}

.polish, .english {
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

.polish:hover, .english:hover {
  background-repeat: no-repeat;
  background-size: cover;
  background-position: top;
}

.polish:hover > *, .english:hover > * {
  display: none;
}

.polish:hover {
  background-image: linear-gradient(rgba(255,255,255,0.5), rgba(255,255,255,0.5)), url("/src/assets/polski.png");
}

.english:hover {
  background-image: linear-gradient(rgba(255,255,255,0.5), rgba(255,255,255,0.5)), url("/src/assets/angielski.png");
}
</style>