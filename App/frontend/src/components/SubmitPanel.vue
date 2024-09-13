<script setup>

</script>

<template>
  <div
      class="submit"
      @click="$emit('showComponent', 1)">
    submit
  </div>
</template>

<style scoped>
.submit {
  width: 80%;
  height: 100%;
  background-color: rgb(248, 249, 250);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  color: #2c3e50;
}
</style>