<script setup>
import {useRouter} from "vue-router";


const router = useRouter()

const response_status = defineModel('response_status')
const props = defineProps(['title', 'subtitle', 'move_to', 'after_create'])


const closeWindow = async () => {
  response_status.value = 0

  if (props.move_to !== undefined) {
    await router.push(props.move_to)
  }
}
</script>

<template>
  <div class="response">
    <div class="header">
      <h3 v-if="response_status >= 100 && response_status <= 199" style="color: black">{{ props.title }}</h3>
      <h3 v-else-if="response_status >= 200 && response_status <= 299" style="color: darkgreen">{{ props.title }}</h3>
      <h3 v-else-if="response_status >= 300 && response_status <= 399" style="color: black">{{ props.title }}</h3>
      <h3 v-else style="color: darkred">{{ props.title }}</h3>
      <div
        class="show-content"
        @click="closeWindow"
        title="Kliknij, aby zamknąć"
      ></div>
    </div>
    <div class="content">
      <h3 v-if="props.subtitle.length !== 0">{{ props.subtitle }}</h3>
      <div class="text">
        <div class="row" v-for="row in after_create" :key="row">
          <div class="element" v-for="element in row" :key="element" v-if="typeof row !== 'string'">{{ element }}</div>
          <div class="element" v-else>{{ row }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.header, .row, .text {
  display: flex;
  align-items: center;
}

.header, .row {
  flex-direction: row;
  justify-content: space-between;
}

.response {
  position: fixed;
  top: 0;
  width: 90%;
  height: 70%;
  padding: 2rem;
  background-color: rgba(245, 245, 245, 0.95);
  border-radius: 1rem;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  color: #333;
  animation: slide-down 0.7s ease-in;
  overflow-y: auto;
}

.header {
  height: 20%;
  border-bottom: 1px solid #ccc;
}

.header h3 {
  font-size: 1.5vw;
  margin: 0;
  color: darkred;
}

.show-content {
  background-color: red;
  height: 2.5vw;
  width: 2.5vw;
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
  overflow-y: auto;
}

.text {
  width: 100%;
  flex-direction: column;
  justify-content: center;
}

.row {
  width: 100%;
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

@media (max-width: 700px) {
  .response {
    padding: 1.5rem;
    font-size: 1.75vh;
  }

  .header > h3 {
    font-size: 1.75vh;
  }

  .show-content {
    height: 2.5vh;
    width: 2.5vh;
  }
}
</style>
