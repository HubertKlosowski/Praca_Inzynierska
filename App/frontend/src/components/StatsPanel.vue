<script setup>
import { inject, onMounted } from 'vue'

const $cookies = inject('$cookies')

const setColor = () => {
  const elements = document.getElementsByClassName('confusion_matrix_element')

  const values = $cookies.get('confusion_matrix')
  const class_instances = values.map((row) => row.reduce((a, b) => a + b))

  const back_color = values.map((row, i) => row.map((el) => {
    const ratio = el / class_instances[i]
    const r = Math.round((1 - ratio) * 255)
    const hex = r.toString(16).padStart(2, '0')
    return `#${hex}0000`
  })).flat()

  for (let i = 0; i < elements.length; i++) {
    elements[i].style.backgroundColor = back_color[i]
    elements[i].style.color = '#2c3e50'
  }
}

if ($cookies.isKey('confusion_matrix')) {
  onMounted(() => setColor())
}
</script>

<template>
  <div class="stats" v-if="$cookies.isKey('confusion_matrix')">
    <div class="confusion_matrix">
      <div class="matrix_row" v-for="row in $cookies.get('confusion_matrix')" :key="row">
        <div
            class="confusion_matrix_element"
            v-for="(el, index) in row" :key="index"
        >
          {{ el }}
        </div>
      </div>
    </div>
    <div class="metrics">
      <div class="metric" v-for="(value, key) in $cookies.get('metrics')" :key="key">
        {{ key }}: {{ value.toFixed(3) }}
      </div>
    </div>
  </div>
  <div class="stats" v-else>
    BŁĄD!! Brak statystyk.<br>Nie wysłałeś/aś żadnych plików do sprawdzenia.
  </div>
</template>

<style scoped>
.stats {
  width: 90%;
  height: 100vh;
  background-color: rgb(248, 249, 250);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  color: #2c3e50;
  text-align: center;
  align-content: center;
  font-size: 1.5rem;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
}

.confusion_matrix, .metrics {
  width: 45%;
  height: 50%;
}

.metrics {
  text-align: center;
  align-content: center;
}

.matrix_row {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
  width: 100%;
  height: 50%;
}

.confusion_matrix_element {
  width: 50%;
  height: 100%;
  background-color: white;
  align-content: center;
  text-align: center;
}

.metric {
  display: flex;
}
</style>