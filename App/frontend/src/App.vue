<script setup>
import MainPage from '@/components/RouterView.vue'
import Footer from '@/components/Footer.vue'
import Header from '@/components/Header.vue'

</script>

<template>
  <div class="container">
    <Header></Header>
    <MainPage></MainPage>
    <Footer></Footer>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  margin: 0;
  font-family: Arial, sans-serif;
}
</style>

