<script setup>
const errors = defineModel()
</script>

<template>
  <div class="error">
    <div class="header">
      <h3>Problem z podanymi danymi</h3>
      <div
        class="show-content"
        @click="errors = []"
        title="Kliknij, aby zamknąć"
      ></div>
    </div>
    <div class="content">
      <h4>Dane przekazane do formularza są błędne. Proszę je poprawić, zgodnie z komunikatami wyświetlanymi poniżej:</h4>
      <ul>
        <li v-for="error in errors" :key="error">
          {{ error }}
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.error {
  position: fixed;
  top: 20%;
  width: 90%;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.95);
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
  .error {
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
