<script setup>
import {ref} from "vue";

const choose = ref(true)
const data = ref(null)
const is_dragging = ref(false)
const info = ref('')
const confirm = ref(false)

const validateData = () => {
  if (typeof data.value === 'object') {
    if (data.value.type !== 'text/csv') {
      info.value = 'BŁĄD!! Plik musi być w rozszerzeniu .csv.'
      data.value = null
    } else if (data.value.size > 20000) {
      info.value = 'BŁĄD!! Plik musi mniejszy od 20KB.'
      data.value = null
    }
  } else if (typeof data.value === 'string') {

  } else {

  }
  confirm.value = true
}

const changeDragging = () => {
  is_dragging.value = !is_dragging.value
}

const drop = (event) => {
  changeDragging()
  data.value = event.dataTransfer.files[0]
  //axios sprawdzenie pliku
}
</script>

<template>
  <div class="left-part">
    <div class="header">
     <div class="choose" @click="choose = !choose">
       <div :class="['circle', { active: choose }]"></div>
     </div>
    </div>
    <div class="depression-form" v-if="choose">
      <form @submit.prevent="validateData">
        <div class="form-row">
          <label for="data" class="text-label">Wpisz tekst do klasyfikacji depresji</label>
          <textarea id="data" v-model="data" placeholder="Tekst" class="form-textarea"></textarea>
          <button type="submit" class="confirm">Zatwierdź</button>
        </div>
      </form>
    </div>
    <div class="depression-form" v-else>
      <form @submit.prevent="validateData">
        <div class="form-row">
          <div
            @dragenter.prevent="changeDragging"
            @dragleave.prevent="changeDragging"
            @dragover.prevent
            @drop.prevent="drop"
            :class="{ 'drag-in': is_dragging, 'drag-out': !is_dragging }">
              <span>Upuść plik</span>
              <span>albo</span>
              <label for="data" class="file-label">Wybierz plik</label>
              <input type="file" id="data" :style="{display: 'none'}">
          </div>
          <button type="submit" class="confirm">Zatwierdź</button>
        </div>
      </form>
    </div>
    <div class="buttons">
      <RouterLink to="/" class="router-link">Wróć</RouterLink>
      <RouterLink to="/models" class="router-link" :style="{visibility: confirm !== true ? 'visible' : 'hidden'}">Dalej</RouterLink>
    </div>
 </div>
</template>

<style scoped>
form {
  height: 100%;
  width: auto;
  margin: 1rem;
}

.drag-in, .drag-out {
  width: auto;
  border-radius: 0.75rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.7);
  text-align: center;
  align-content: center;
}

.drag-in, .drag-out {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.drag-in > *, .drag-out > * {
  margin: 1%;
}

.drag-in {
  background-color: gray;
  border: 3px dashed black;
}

.drag-out {
  background-color: lightgray;
  border: 3px solid black;
}

.left-part {
  width: 90%;
  height: auto;
  flex-direction: row;
}

.header {
  width: 100%;
  height: 20%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.choose {
  width: 10rem;
  height: 3rem;
  background-color: #ccc;
  border-radius: 1.5rem;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: background-color 0.3s ease;
  position: relative;
}

.choose:hover {
  background-color: #bbb;
}

.circle {
  width: 2.5rem;
  height: 2.5rem;
  background-color: whitesmoke;
  border-radius: 50%;
  border: 2px solid black;
  margin-left: 0.25rem;
  transition: transform 0.3s ease, background-color 0.3s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.circle.active {
  transform: translateX(7rem);
  background-color: #4CAF50;
  border-color: #4CAF50;
}

.buttons {
  width: 100%;
  height: 20%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}

.depression-form {
  width: 70%;
  height: 60%;
  margin: 0 auto;
  padding: 2rem;
  background-color: #f5f5f5;
  border-radius: 0.75rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  height: 100%;
}

.text-label {
  font-size: 1.5vw;
  color: #333;
  font-weight: bold;
}

.file-label {
  padding: 0.5rem;
  border-radius: 1rem;
  border: 2px solid black;
  font-size: 1.35vw;
  background-color: lightgrey;
  transition: 0.4s ease;
}

.file-label:hover {
  color: white;
  border: 2px solid white;
  background-color: darkgrey;
  box-shadow: 1rem 1rem mediumpurple;
}

span {
  font-size: 1.5vw;
  color: #333;
}

.form-textarea {
  width: auto;
  height: 20%;
  min-height: 10%;
  max-height: 60%;
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

.confirm {
  padding: 0.75rem 1.5rem;
  font-size: 1.25vw;
  color: white;
  background-color: #4682B4;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.confirm:hover {
  background-color: #3a6a9b;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>