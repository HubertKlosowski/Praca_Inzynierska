<script setup>

</script>

<template>
  <div
      class="chat"
      @click="$emit('showComponent', 2)">
    chat
  </div>
</template>

<style scoped>
.chat {
  width: 80%;
  height: 100%;
  background-color: rgb(248, 249, 250);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  color: #2c3e50;
}
</style>