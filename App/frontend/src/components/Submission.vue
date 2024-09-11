<script setup>
const makeBigger = (param) => {
  const element = document.getElementsByClassName(param)[0]
  console.log(element)
}
</script>

<template>
  <div class="submission">
    <div class="requirements" @click="makeBigger('requirements')">

    </div>
    <div class="submit" @click="makeBigger('submit')">

    </div>
    <div class="choose_model" @click="makeBigger('choose_model')">

    </div>
    <div class="stats" @click="makeBigger('stats')">

    </div>
  </div>
</template>

<style scoped>
.submission {
  width: 80%;
  padding: 20px;
  height: 90%;
  margin: 0 auto;
  background-color: lightsteelblue;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-evenly;
  flex-wrap: wrap;
}

.submit, .choose_model, .stats, .requirements {
  width: 40%;
  height: 40%;
  background-color: rgb(248, 249, 250);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>