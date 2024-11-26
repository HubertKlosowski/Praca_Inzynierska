<script setup>
import {ref, watch} from "vue";

const props = defineProps(['label_info', 'label_name'])
const emits = defineEmits(['update_variable'])
const variable = ref('')

watch(variable, () => {
  emits('update_variable', variable.value)
})
</script>

<template>
  <div class="form-row">
    <label :for="label_name">{{ label_info }}</label>
    <input type="text" :id="label_name" v-model="variable" :placeholder="label_info"/>
  </div>
</template>

<style scoped>
.form-row {
  width: 70%;
  height: 100px;
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

label {
  width: 70%;
  height: 45%;
  font-size: 1.75vw;
  padding: 1rem;
}

input[type="text"] {
  width: 70%;
  height: 45%;
  font-size: 1.75vw;
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
