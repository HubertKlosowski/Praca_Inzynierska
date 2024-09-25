<script setup>
import { ref } from 'vue'

const llm_model = ref('')
const file = ref(null)

const handleFile = (event) => {
  file.value = event.target.files[0]
}
</script>

<template>
  <div class="form">
    <form @submit.prevent="$emit('sendData', ([llm_model, file]))">
      <h2>Wybierz model językowy</h2>
      <div class="radio_row">
        <div class="radio_item">
          <input type="radio" id="bert-base" value="bert-base" v-model="llm_model">
          <label for="bert-base">BERT-BASE</label>
        </div>
        <div class="radio_item">
          <input type="radio" id="bert-large" value="bert-large" v-model="llm_model">
          <label for="bert-large">BERT-LARGE</label>
        </div>
      </div>
      <label for="file">Wybierz plik</label>
      <input type="file" id="file" @change="handleFile"/>
      <button type="submit">Wyślij</button>
    </form>
  </div>
</template>

<style scoped>
.form {
  width: 65%;
}

h2 {
  margin-bottom: 20px;
  font-size: 1.5rem;
  color: white;
}

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 20px;
  background-color: #00247D;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.radio_row {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
}

.radio_item {
  display: flex;
  align-items: center;
}

.radio_item label {
  margin-left: 10px;
  font-size: 1rem;
  color: white;
}

label {
  font-weight: bold;
  margin-bottom: 8px;
  color: white;
}

input[type="radio"] {
  width: 1.2rem;
  height: 1.2rem;
  transform: translateY(-0.35em) translateX(0.35rem);
}

input[type="file"] {
  margin-top: 10px;
  padding: 8px;
  border: 1px solid #cf142b;
  border-radius: 4px;
  font-size: 1rem;
}

button[type="submit"] {
  padding: 10px;
  margin-top: 15px;
  background-color: #cf142b;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button[type="submit"]:hover {
  background-color: #e6001f;
}
</style>