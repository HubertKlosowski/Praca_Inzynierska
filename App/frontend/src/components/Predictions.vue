<script setup>
// dodaj pasek progresu
</script>

<template>
 <div class="left-part">
   <div class="buttons">
     <RouterLink to="/models" class="router-link">Wróć</RouterLink>
     <RouterLink to="/" class="router-link">Powrót do strony głównej</RouterLink>
    </div>
 </div>
</template>

<style scoped>
.left-part {
  width: 90%;
}

.buttons {
  width: 100%;
  height: 20%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}
</style>