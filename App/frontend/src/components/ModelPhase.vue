<script setup>
import {onMounted, onUpdated, ref} from "vue"
import ModelIntro from "@/components/ModelIntro.vue";
import polish from "@/assets/polski.png";
import english from "@/assets/angielski.png";

const props = defineProps(['phase', 'num_phase'])

const show_intro = ref(true)

const choosen_language = ref('')
const choosen_version = ref('')

const deleteChildElements = (parent) => {
  while (parent.firstChild) {
    parent.removeChild(parent.lastChild)
  }
}

const setVersion = (param) => {

}

const setLanguage = (param) => {
  choosen_language.value = param

  const element = document.getElementsByClassName(param)[0]
  element.style.border = '2px solid black'
  element.style.backgroundImage = `url(${param === 'polish' ? polish : english})`
  element.style.backgroundRepeat = 'no-repeat'
  element.style.backgroundSize = 'cover'
  element.style.backgroundPosition = 'top'

  deleteChildElements(element)

  // dodaj tekst "wybrałeś język ..."
}

onUpdated(() => {
  if (show_intro.value) {
    const magic = document.querySelector('.magic')
    magic.removeEventListener('animationend', () => { show_intro.value = false })
    magic.addEventListener('animationend', () => { show_intro.value = false })
  }
})

onMounted(() => {
  const magic = document.querySelector('.magic')
  magic.addEventListener('animationend', () => { show_intro.value = false })
})
</script>

<template>
  <ModelIntro v-if="show_intro" :phase="props.phase"></ModelIntro>
  <div class="model" v-else :style="{height: props.num_phase === 3 ? '68%' : '83%'}">
    <div class="header">
      <div class="buttons">
        <button
            type="button"
            class="router-link"
            :disabled="props.num_phase === 0"
            @click="() => {
              show_intro = true
              $emit('previousOne', props.num_phase - 1)
            }"
        >Wróć</button>
        <button
            type="button"
            class="router-link"
            :disabled="props.num_phase === 3"
            @click="() => {
              show_intro = true
              $emit('nextOne', props.num_phase + 1)
            }"
        >Dalej</button>
      </div>
      <div class="icon fa fa-question-circle" @click.prevent="show_intro = !show_intro"></div>
    </div>
    <div class="main" v-if="props.num_phase === 0">
      <div class="phases">
        <h3>Etapy konfiguracji modelu:</h3>
        <ul>
          <li>Wstęp</li>
          <li>Wybór wersji językowej</li>
          <li>Wybór wersja modelu</li>
          <li>Zatwierdzenie</li>
        </ul>
      </div>
      <div class="phases-description">
        <h3>Opis:</h3>
        <p>W tej sekcji możesz zapoznać się z procesem wyboru i konfiguracji modelu.</p>
        <p>Przed przejściem do kolejnego etapu zostanie wyświetlony jego krótki opis.</p>
        <p>W nagłówku wyświetlane jest twoje położenie na stronie.
          Koło oznaczone na czerwono wskazuje obecnie wyświetlany etap.</p>
        <p>Ikonka znaku zapytania umożliwia powrót od opisu, jeśli istnieje taka potrzeba.</p>
        <p>W trakcie przechodzenia przez etapy musisz wybrać elementy konfiguracji swojego modelu.</p>
        <p>Twoje wybory zostaną przedstawione w ostatnim etapie.</p>
      </div>
    </div>
    <div class="main" v-if="props.num_phase === 1">
      <div class="polish" @click="setLanguage('polish')">
        <p>
          Wszystkie języki różnią się od siebie.
          Gramatyka, słownictwo, sposób zapisu zdań ma gigantyczny wpływ na wskazanie emocji w tekście.
        </p>
        <p>
          Modele podobnie jak my ludzie muszą się nauczyć języka aby móc go "rozumieć".
          Jeśli nauczą się jednego języka, np. polskiego nie są w stanie bez wcześniejszego przygotowania rozumieć słów w innym języku.
        </p>
      </div>
      <div class="english" @click="setLanguage('english')">
        <p>
          Nieprawidłowo wybrany język może spowodować otrzymanie błędnych wyników w predykcjach.
          Dlatego tak ważnym jest wybranie modelu pod języku przekazanych danych.
        </p>
        <p style="font-weight: bold">
          Kliknij w jeden z tych przycisków aby wybrać język polski (po lewej) albo język angielski (po prawej).
        </p>
      </div>
    </div>
    <div class="main" v-if="props.num_phase === 2">
      <div class="base" @click="setVersion('base')">
        <h3>Wersja podstawowa</h3>
        <ul>
          <li>szybszy czas wykonania</li>
          <li>podstawowe zrozumienie danych tekstowych</li>
        </ul>
      </div>
      <div class="large" @click="setVersion('large')">
        <h3>Wersja rozbudowana</h3>
        <ul>
          <li>większą dokładność wyników.</li>
          <li>lepsze zrozumienie danych tekstowych</li>
          <li>3 razy większy o wersji podstawowej</li>
        </ul>
      </div>
    </div>
    <div class="main" v-if="props.num_phase === 3">
      <div class="text">
        <p>Proces konfiguracji zakończony pomyślnie.</p>
        <p>Model rozpoczął przetwarzanie danych.</p>
      </div>
      <div class="choosen-options">
        <p>Wybrane opcje:</p>
        <ul>
          <li>Język: {{ props.language }}</li>
          <li>Model: {{ props.modelType }}</li>
          <li>Wersja: {{ props.version }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.header {
  height: 20%;
  display: flex;
  flex-direction: row;
  justify-content: end;
  align-items: center;
  background-color: #bbb;
}

.router-link {
  height: 200%;
}

.phases, .phases-description, .polish, .english, .base, .large, .text, .choosen-options {
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

.polish:hover, .english:hover, .base:hover, .large:hover {
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

.base:hover {
  background-image: linear-gradient(rgba(255,255,255,0.5), rgba(255,255,255,0.5)), url("/src/assets/base.png");
}

.large:hover {
  background-image: linear-gradient(rgba(255,255,255,0.5), rgba(255,255,255,0.5)), url("/src/assets/large.png");
}

.main {
  height: 80%;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
}

.buttons {
  width: 90%;
  height: 30%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}

.icon {
  width: 10%;
  font-size: 300%;
  text-align: center;
}

.model {
  height: 70%;
  width: 100%;
  display: flex;
  flex-direction: column;
}
</style>