<script setup>
import {inject, onMounted, ref} from "vue";

const $cookies = inject('$cookies')
const model_text = ref([])
const show = ref(true)
const current = defineModel('current')

const modelConfigDescription = () => {
  const lang = $cookies.get('model_language') === 'polish' ? 'polskim' : 'angielskim'
  const version = $cookies.get('model_version') === 'base' ? 'podstawowej' : 'rozszerzonej'
  let text = 'Konfiguracja modelu pozwala mu na pracę z danymi w języku ' + lang + '. ' +
      'Obecnie jest wybrany model w wersji ' + version + '. '
  if (version === 'podstawowej') {
    text += 'Wybrałeś szybkość rozwiązania od jego dokładności.'
  } else {
    text += 'Osiągniesz lepszą dokładność, niestety kosztem dłuższego czasu wykonania. Taka konfiguracja zalecana jest dla mniejszych zbiorów.'
  }

  text = text.split('.')
  text.pop()

  for (let i = 0; i < text.length; i++) {
    text[i] += '.'
  }

  return text
}

onMounted(() => {
  model_text.value = modelConfigDescription()
  current.value = 3
})
</script>

<template>
  <div class="main">
    <div class="text">
      <span>
        Proces konfiguracji modelu został zakończony pomyślnie.
        Model jest gotowy do pracy. &#128578;
      </span>
    </div>
    <div class="more-info">
      <div class="manage">
        <h3>Informacje o konfiguracji modelu</h3>
        <div class="show-content" @click="show = !show" :style="{ backgroundColor: show ? 'green' : 'red' }"></div>
      </div>
      <div class="content-model" :class="{ visible: show, hidden: !show }">
        <span v-for="sentence in model_text" :key="sentence">{{ sentence }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.manage {
  width: 90%;
  height: 20%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}

.more-info {
  justify-content: center;
  align-items: center;
}

.content-model {
  width: 90%;
  height: 60%;
  flex-direction: column;
  justify-content: center;
  background-color: gray;
  color: white;
  padding: 1rem;
  border-radius: 0.75rem;
}

.content-model {
  overflow-y: auto;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.5s ease, visibility 0.5s ease;
}

.content-model.visible {
  opacity: 1;
  visibility: visible;
}

.content-model.hidden {
  opacity: 0;
  visibility: hidden;
}

.show-content {
  height: 20px;
  width: 20px;
  border-radius: 50%;
}

.main {
  width: 100%;
  height: 80%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}

@media (max-width: 768px) {
  .main {
    flex-direction: column;
    font-size: 1.75vh;
  }

  .main * {
    font-size: 1.75vh !important;
  }

  .text, .more-info {
    width: 80% !important;
    height: 30% !important;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
  }
}

.text, .more-info {
  width: 40%;
  height: 80%;
  margin: 0 auto;
  background-color: #f5f5f5;
  border-radius: 0.75rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 1.5rem;
}
</style>