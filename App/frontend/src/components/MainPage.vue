<script setup>
import {RouterView} from "vue-router";

</script>

<template>
  <div class="main">
    <RouterView></RouterView>
  </div>
</template>

<style scoped>
.main {
  flex: 3;
  background-color: #34495e;
  color: white;
  padding: 20px;
}
</style>