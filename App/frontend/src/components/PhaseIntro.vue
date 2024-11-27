<script setup>
import {ref} from "vue";

const props = defineProps(['phase'])

const pause = ref(false)
</script>

<template>
  <div class="model">
    <div class="description">
      <div class="title">
        <h3>{{ props.phase.title }}</h3>
      </div>
      <div class="content">
        <p v-for="line in props.phase.description">{{ line }}</p>
      </div>
    </div>
    <div class="bar">
      <div class="magic" :style="{animationPlayState: !pause ? 'running' : 'paused'}"></div>
    </div>
    <div class="pause">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512" @click="pause = !pause" v-if="pause">
        <path d="M73 39c-14.8-9.1-33.4-9.4-48.5-.9S0 62.6 0 80L0 432c0 17.4 9.4 33.4 24.5 41.9s33.7 8.1 48.5-.9L361 297c14.3-8.7 23-24.2 23-41s-8.7-32.2-23-41L73 39z"/>
      </svg>
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" @click="pause = !pause" v-else>
        <path d="M48 64C21.5 64 0 85.5 0 112L0 400c0 26.5 21.5 48 48 48l32 0c26.5 0 48-21.5 48-48l0-288c0-26.5-21.5-48-48-48L48 64zm192 0c-26.5 0-48 21.5-48 48l0 288c0 26.5 21.5 48 48 48l32 0c26.5 0 48-21.5 48-48l0-288c0-26.5-21.5-48-48-48l-32 0z"/>
      </svg>
    </div>
  </div>
</template>

<style scoped>
svg {
  height: 9vh;
  width: 9vw;
  border: 2px solid black;
}

.pause {
  height: 20%;
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

@media (max-width: 768px) {
  .model {
    font-size: 1.75vh;
  }

  .model * {
    font-size: 1.75vh !important;
  }
}

@keyframes progress-bar {
  0% {
    width: 100%;
    background-color: green;
  }
  50% {
    width: 50%;
    background-color: #FFEA00;
  }
  100% {
    width: 0;
    background-color: red;
  }
}

.bar {
  height: 10%;
  width: 100%;
}

.magic {
  height: 100%;
  border-radius: 1rem;
  animation: progress-bar 5ms ease-in-out;
  position: relative;
}

.description {
  height: 80%;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: rgba(245, 245, 245, 0);
  border-radius: 0.75rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.7);
  gap: 1.5rem;
}

.title, .content {
  width: 90%;
  background-color: lightgray;
  border-radius: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.title {
  height: 20%;
}

.content {
  height: 50%;
  padding: 1rem;
}
</style>