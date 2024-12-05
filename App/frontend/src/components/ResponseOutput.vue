<script setup>
const after_create = defineModel('after_create')
const response_status = defineModel('response_status')

const props = defineProps(['title'])

const closeWindow = () => {
  after_create.value = {}
  response_status.value = 0
}
</script>

<template>
  <div class="response">
    <div class="header">
      <h3 :style="{ color: response_status >= 200 && response_status <= 299 ? 'darkgreen' : 'darkred' }">{{ props.title }}</h3>
      <div
        class="show-content"
        @click="closeWindow"
        title="Kliknij, aby zamknąć"
      ></div>
    </div>
    <div class="content">
      <h3 v-if="response_status >= 200 && response_status <= 299">Dane użytkownika</h3>
      <h3 v-else-if="response_status >= 300 && response_status <= 499">Dane przekazane do formularza są błędne. Proszę je poprawić, zgodnie z komunikatami wyświetlanymi poniżej:</h3>
      <h3 v-else>Proszę poczekać, serwer nie jest teraz dostępny.</h3>
      <ul>
        <li v-for="sentence in after_create" :key="sentence">
          {{ sentence }}
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.response {
  position: fixed;
  top: 20%;
  width: 90%;
  padding: 2rem;
  background-color: rgba(245, 245, 245, 0.95);
  border-radius: 1rem;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  color: #333;
  animation: slide-down 0.7s ease-in;
}

@keyframes slide-down {
  0% {
    transform: translateY(-60%);
    opacity: 0;
  }
  100% {
    transform: translateY(0%);
    opacity: 1;
  }
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  border-bottom: 1px solid #ccc;
  padding-bottom: 0.5rem;
}

.header h3 {
  font-size: 1.25rem;
  margin: 0;
  color: darkred;
}

.show-content {
  background-color: red;
  height: 40px;
  width: 40px;
  border-radius: 50%;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.show-content:hover {
  transform: scale(1.1);
}

.content {
  text-align: left;
  background-color: #f5f5f5;
  padding: 1rem;
  border-radius: 0.5rem;
}

.content h4 {
  font-size: 1rem;
  margin: 0 0 1rem 0;
  color: #333;
}

.content ul {
  list-style-type: disc;
  margin: 0;
  padding-left: 1.5rem;
}

.content li {
  font-size: 0.9rem;
  color: #333;
  margin-bottom: 0.5rem;
}

@media (max-width: 768px) {
  .response {
    padding: 1.5rem;
    font-size: 1.75vh;
  }

  .header h3 {
    font-size: 1.75vh;
  }

  .show-content {
    height: 35px;
    width: 35px;
  }

  .content h4 {
    font-size: 1.5vh;
  }

  .content li {
    font-size: 1.5vh;
  }
}
</style>
