<script setup>
const props = defineProps(['phase'])

const show_intro = defineModel('show_intro')
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
      <font-awesome-icon :icon="['fas', 'forward']" @click="show_intro = !show_intro" />
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