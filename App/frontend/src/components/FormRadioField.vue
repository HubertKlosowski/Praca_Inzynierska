<script setup>
const input_value = defineModel('input_value')

const props = defineProps(['title', 'options', 'values'])
</script>

<template>
  <div class="form-row">
    <div class="title">
      <span>{{ props.title }}</span>
    </div>
    <div class="radio-column">
      <div class="radio-row">
        <label :for="option" v-for="option in props.options" :key="option">{{ option }}</label>
      </div>
      <div class="radio-row">
        <input type="radio" :id="option" v-for="(option, i) in props.options" :value="props.values[i]" v-model="input_value" :key="option">
      </div>
    </div>
  </div>
</template>

<style scoped>
label, span {
  font-size: 1.5vw;
}

.radio-row {
  width: 80%;
  height: 30%;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
}

.form-row {
  width: 80%;
  height: 20%;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
  background-color: #f5f5f5;
  border-radius: 0.75rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.7);
  margin: 1rem;
  padding: 1rem;
}

.title {
  width: 30%;
}

.radio-column {
  width: 70%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}

input[type="radio"] {
  border: 0;
  width: 100%;
  height: 1.5vw;
}

@media (max-width: 768px) {
  label, span {
    font-size: 1.5vh;
  }

  input[type="radio"] {
    border: 0;
    width: 100%;
    height: 1.5vh;
  }
}
</style>