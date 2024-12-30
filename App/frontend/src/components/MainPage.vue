<script setup>
import AboutProject from "@/components/AboutProject.vue";
import AboutAccount from "@/components/AboutAccount.vue";
import AboutPredictions from "@/components/AboutPredictions.vue";
import Menu from "@/components/Menu.vue";
import {onMounted, ref} from "vue";


const show_info = ref(1)


onMounted(() => {
  if (localStorage.getItem('user') === null) {
    localStorage.setItem('user', JSON.stringify({}))
  }
})
</script>

<template>
  <AboutProject v-if="show_info === 1"></AboutProject>
  <AboutAccount v-if="show_info === 2"></AboutAccount>
  <AboutPredictions v-if="show_info === 3"></AboutPredictions>
  <Menu v-model:show_info="show_info"></Menu>
</template>

<style scoped>

</style>