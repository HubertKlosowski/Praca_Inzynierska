<script setup>
const model = defineModel()
</script>

<template>
  <div class="form-row">
    <div class="title">
      <span>Typ konta</span>
    </div>
    <div class="radio-column">
      <div class="radio-row">
        <label for="normal">Normal</label>
        <label for="normal">Pro</label>
        <label for="normal">Administrator</label>
      </div>
      <div class="radio-row">
        <input type="radio" id="normal" value="0" v-model="model" checked="checked">
        <input type="radio" id="pro" value="1" v-model="model">
        <input type="radio" id="admin" value="2" v-model="model">
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
  max-width: 90%;
  width: 70%;
  height: 100px;
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
  height: 1.25rem;
  background-color: red;
}

@media (max-width: 768px) {
  label, span {
    font-size: 2vh;
  }
}
</style>