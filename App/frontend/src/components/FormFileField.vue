<script setup>
const is_dragging = defineModel('is_dragging')
const data = defineModel('data')


const changeDragging = () => {
  is_dragging.value = !is_dragging.value
}

const drop = (event) => {
  changeDragging()
  data.value = event.dataTransfer.files[0]
}

const getFile = () => {
  data.value = document.getElementById('data').files[0]
}
</script>

<template>
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
        <input type="file" id="data" @change="getFile" :style="{ display: 'none' }">
    </div>
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

.drag-in, .drag-out {
  width: 90%;
  height: 10rem;
  border-radius: 0.75rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.7);
  text-align: center;
  align-content: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
}

.drag-in {
  background-color: gray;
  border: 3px dashed black;
}

.drag-out {
  background-color: lightgray;
  border: 3px solid black;
}

.file-label {
  padding: 0.5rem;
  border-radius: 1rem;
  border: 2px solid black;
  font-size: 1.5vw;
  background-color: lightgrey;
  transition: 0.4s ease;
  cursor: pointer;
}

.file-label:hover {
  color: white;
  border: 2px solid white;
  background-color: darkgrey;
  box-shadow: 0.5rem 0.5rem dodgerblue;
}

@media (max-height: 550px) {
  .drag-in, .drag-out {
    display: flex;
    flex-direction: row;
    justify-content: space-evenly;
  }
}
</style>