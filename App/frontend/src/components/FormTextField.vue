<script setup>
const props = defineProps(['label_info', 'label_name', 'reset', 'error'])
const model = defineModel()
</script>

<template>
  <div class="form-row">
    <div class="row">
      <label :for="props.label_name">Podaj {{ props.label_info.toLowerCase() }}</label>
      <div class="error"></div>
    </div>
    <input
        v-model="model"
        type="text"
        :id="props.label_name"
        :placeholder="props.label_info"/>
  </div>
</template>

<style scoped>
.form-row {
  width: 70%;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
  background-color: #f5f5f5;
  border-radius: 0.75rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.7);
  margin: 1rem;
  padding: 1rem;
}

.error {
  width: 50%;
  background-color: red;
}

label {
  background-color: #cccccc;
}

.row {
  width: 100%;
  height: 45%;
  font-size: 1.5vw;
  padding: 1rem;
}

input[type="text"] {
  width: 100%;
  height: 70%;
  font-size: 1.5vw;
  box-sizing: border-box;
  padding: 1rem;
  border-radius: 0.75rem;
}

@media (max-width: 768px) {
  .form-row {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  input[type="text"] {
    height: 70%;
    width: 100%;
    font-size: 2vh;
  }

  label {
    display: none;
  }
}
</style>
