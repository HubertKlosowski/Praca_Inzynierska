<script setup>
const props = defineProps(['phase'])

const show_intro = defineModel()
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
    <div class="pause">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" @click="show_intro = !show_intro">
        <path d="M512 76v360c0 6.6-5.4 12-12 12h-40c-6.6 0-12-5.4-12-12V284.1L276.5 440.6c-20.6 17.2-52.5 2.8-52.5-24.6V284.1L52.5 440.6C31.9 457.8 0 443.4 0 416V96c0-27.4 31.9-41.7 52.5-24.6L224 226.8V96c0-27.4 31.9-41.7 52.5-24.6L448 226.8V76c0-6.6 5.4-12 12-12h40c6.6 0 12 5.4 12 12z"/>
      </svg>
    </div>
  </div>
</template>

<style scoped>
.model {
  height: 70%;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

svg {
  height: 9vh;
  width: 9vw;
  padding: 0 1rem 0 1rem;
  border: 2px solid black;
}

.pause {
  height: 20%;
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}

@keyframes progress-bar {
  0% {
    width: 100%;
    background-color: green;
  }
  50% {
    width: 50%;
    background-color: yellow;
  }
  100% {
    width: 0;
    background-color: red;
  }
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
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 1rem;
}

.title {
  height: 20%;
}

.content {
  height: 50%;
}

@media (max-width: 768px) {
  .model {
    font-size: 1.75vh;
  }

  .model * {
    font-size: 1.75vh !important;
  }
}
</style>