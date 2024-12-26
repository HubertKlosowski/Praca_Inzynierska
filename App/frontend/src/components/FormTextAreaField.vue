<script setup>
const data = defineModel('data')
</script>

<template>
  <div class="form-row">
    <label for="data" class="text-label">Wpisz tekst do klasyfikacji depresji</label>
    <textarea id="data" v-model="data" placeholder="Tekst" class="form-textarea"></textarea>
  </div>
</template>

<style scoped>
.form-row {
  width: 80%;
  height: 10rem;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
  background-color: #f5f5f5;
  border-radius: 0.75rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.7);
  margin: 1rem;
  padding: 1rem;
}

.form-textarea {
  width: 90%;
  height: 10rem;
  padding: 0.75rem;
  font-size: 1.25vw;
  border: 1px solid #ccc;
  border-radius: 0.5rem;
  resize: vertical;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.form-textarea:focus {
  border-color: #4682B4;
  box-shadow: 0 0 5px rgba(70, 130, 180, 0.5);
  outline: none;
}

.text-label {
  font-size: 1.5vw;
  color: #333;
  font-weight: bold;
  padding: 1rem;
}
</style>