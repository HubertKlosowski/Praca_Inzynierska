<script setup>
import {ref} from "vue";
import depression from "@/assets/depression.jpg";

const show_info = ref(1)

// https://www.amahahealth.com/blog/understanding-depression-signs-causes-and-types/
</script>

<template>
  <div class="right-part" :style="{
      backgroundImage: `url(${depression})`,
      backgroundRepeat: 'no-repeat',
      backgroundSize: 'cover'}">
    <div class="buttons">
      <button type="button" class="main-button" @click="$emit('emitShowInfo', 1); show_info = 1"
              :style="{
        backgroundColor: show_info === 1 ? 'darkgrey' : 'lightgrey',
        color: show_info === 1 ? 'white' : 'black',
        border: show_info === 1 ? 'none' : '2px solid black'}">O projekcie</button>
      <button type="button" class="main-button" @click="$emit('emitShowInfo', 2); show_info = 2"
              :style="{
        backgroundColor: show_info === 2 ? 'darkgrey' : 'lightgrey',
        color: show_info === 2 ? 'white' : 'black',
        border: show_info === 2 ? 'none' : '2px solid black'}">Twoje konto</button>
      <button type="button" class="main-button" @click="$emit('emitShowInfo', 3); show_info = 3"
              :style="{
        backgroundColor: show_info === 3 ? 'darkgrey' : 'lightgrey',
        color: show_info === 3 ? 'white' : 'black',
        border: show_info === 3 ? 'none' : '2px solid black'}">Sprawdź posty</button>
    </div>
  </div>
</template>

<style scoped>
.buttons {
  height: 100%;
  width: 100%;
  background-color: rgba(245, 245, 245, 0.5);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

button {
  width: 50%;
  height: 20%;
  margin: 1rem;
  font-size: 1.5vw;
  border-radius: 1rem;
  transition: 0.4s ease;
}

button:hover {
  background-color: darkgrey;
  box-shadow: 1rem 1rem mediumpurple;
}

.right-part {
  width: 45%;
  height: 95%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-bottom-left-radius: 1rem;
  border-top-left-radius: 1rem;
  border: 2px solid mediumpurple;
  margin: 1%;
}
</style>