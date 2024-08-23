<script setup>
import { RouterView } from "vue-router";

</script>

<template>
  <div class="container">
    <div class="header">
      <div class="project_info">
      </div>
      <div class="links">
        <RouterLink to="/">
          <img src="./assets/home.png" alt="Strona główna">
        </RouterLink>
        <RouterLink to="/details">
          <img src="./assets/details.png" alt="Szczegóły projektu">
        </RouterLink>
        <RouterLink to='/login'>
          <img src="./assets/user.png" alt="Konto">
        </RouterLink>
      </div>
    </div>
    <div class="main">
      <RouterView></RouterView>
    </div>
    <div class="footer">
      Footer
    </div>
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

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #2c3e50;
  color: white;
  padding: 10px 20px;
}

.project_info {
  display: flex;
  gap: 20px;
}

.links {
  display: flex;
  gap: 15px;
}

img {
  max-width: 30px;
  height: auto;
  cursor: pointer;
}

.main {
  flex: 3;
  background-color: #34495e;
  color: white;
  padding: 20px;
}

.footer {
  flex: 0.5;
  background-color: #16a085;
  color: white;
  text-align: center;
  padding: 10px 0;
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

