<script setup>
const props = defineProps(['phase'])
</script>

<template>
  <div class="model">
    <div class="description">
      <div class="title">
        {{ props.phase.title }}
      </div>
      <div class="content">
        <p v-for="line in props.phase.description">{{ line }}</p>
      </div>
    </div>
    <div class="bar">
      <div class="magic"></div>
    </div>
  </div>
</template>

<style scoped>
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
  animation: progress-bar 1s ease-in-out;
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
}
</style>