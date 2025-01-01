<script setup>
import depression from "@/assets/depression.jpg";

const show_info = defineModel('show_info')

// https://www.amahahealth.com/blog/understanding-depression-signs-causes-and-types/
</script>

<template>
  <div class="right-part" :style="{
      backgroundImage: `url(${depression})`,
      backgroundRepeat: 'no-repeat',
      backgroundSize: 'cover',
      backgroundPosition: 'center'
  }">
    <div class="buttons">
      <button type="button" class="router-link" @click="show_info = 1">O projekcie</button>
      <button type="button" class="router-link" @click="show_info = 2">Twoje konto</button>
      <button type="button" class="router-link" @click="show_info = 3">Twoje predykcje</button>
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
  border: 2px solid dodgerblue;
  margin: 1%;
}

@media (max-width: 700px) {
  .right-part {
    width: 90%;
    height: 45%;
    font-size: 1.75vh;
  }

  .right-part * {
    font-size: 1.75vh !important;
  }
}
</style>