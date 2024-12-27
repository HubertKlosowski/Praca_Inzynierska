<script setup>
const props = defineProps(['login'])

const emits = defineEmits(['redEvent'])
</script>

<template>
  <div class="form-row">
    <button type="submit" class="green">
      <slot name="green"></slot>
    </button>
    <button type="button" class="red" v-if="!props.login" @click="emits('redEvent')">
      <slot name="red"></slot>
    </button>
  </div>
</template>

<style scoped>
.form-row {
  width: 80%;
  height: 20%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
  border-radius: 0.75rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.7);
  margin: 1rem;
  padding: 1rem;
}

.green, .red {
  text-decoration: none;
  text-align: center;
  align-content: center;
  margin: 1rem;
  font-size: 1.5vw;
  transition: 0.4s ease;
  cursor: pointer;
  background-color: white;
  border-radius: 1rem;
  width: 40%;
  height: 70%;
}

.green:hover, .red:hover {
  color: white;
  border: 2px solid white;
  box-shadow: 0.5rem 0.5rem dodgerblue;
}

.green:hover {
  background-color: darkgreen;
}

.red:hover {
  background-color: darkred;
}

.green {
  border: 2px solid green;
  color: green;
}

.red {
  border: 2px solid red;
  color: red;
}

@media (max-width: 700px) {
  .form-row > * {
    width: 70%;
    font-size: 1.5vh;
  }
}
</style>