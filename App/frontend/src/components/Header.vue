<script setup>
import { inject } from 'vue'

const $cookies = inject('$cookies')
</script>

<template>
  <div class="header">
    <div class="project_info">
      <img src="@/assets/logo.png" alt="Logo" id="logo">
      <h2>Aplikacja do wykrycia depresji</h2>
    </div>
    <div class="links">
      <RouterLink to="/submissions" v-if="$cookies.isKey('user')">
        <img src="@/assets/submit.png" alt="Submission">
      </RouterLink>
      <RouterLink to="/">
        <img src="@/assets/home.png" alt="Strona główna">
      </RouterLink>
      <RouterLink to="/details">
        <img src="@/assets/details.png" alt="Szczegóły projektu">
      </RouterLink>
      <RouterLink to='/login'>
        <img src="@/assets/user.png" alt="Logowanie">
      </RouterLink>
    </div>
  </div>
</template>

<style scoped>
.links > * {
  position: relative;
  animation-name: toTheRight;
  animation-duration: 4s;
  animation-timing-function: ease-out;
  animation-direction: reverse;
}

#logo {
  max-width: 100px;
  height: auto;
  position: relative;
  animation-name: toTheLeft;
  animation-duration: 4s;
  animation-timing-function: ease-out;
  animation-direction: reverse;
}

h2 {
  transform: translateY(0.5rem);
  position: relative;
  animation-name: toTheLeft;
  animation-duration: 4s;
  animation-timing-function: ease-out;
  animation-direction: reverse;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: lightblue;
  color: white;
  padding: 10px 20px;
  border-bottom: 2px black solid;
}

.project_info {
  display: flex;
  gap: 20px;
}

.links {
  display: flex;
  gap: 15px;
}

img:not(#logo) {
  max-width: 30px;
  height: auto;
  cursor: pointer;
}

a {
  text-decoration: none;
  color: #2c3e50;
  background-color: #ecf0f1;
  border: 2px solid #bdc3c7;
  padding: 8px 12px;
  margin: 0 5px;
  border-radius: 5px;
  transition: background-color 0.3s, color 0.3s;
}

a:hover {
  background-color: #bdc3c7;
  color: #2c3e50;
}
</style>