<script setup>
import {reactive} from "vue";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";


const user = reactive(JSON.parse(localStorage.getItem('user')))
</script>

<template>

  <div class="left-part">
    <div class="header">
      <h3>Limity konta</h3>
      <ul>
        <li>Każde konto posiada określone limity.</li>
      </ul>
    </div>
    <div class="go-main">
      <RouterLink to="/profile" class="router-link">
        <font-awesome-icon :icon="['fas', 'user']" />
      </RouterLink>
    </div>
    <div class="limits">
      <div class="header-limit">
        <div class="info" style="font-weight: bold">Funkcjonalność</div>
        <div class="info" style="font-weight: bold">Limit</div>
      </div>
      <div class="limit">
        <div class="info">Logowanie</div>
        <div class="info">5 na godzinę</div>
      </div>
      <div class="limit">
        <div class="info">Usunięcie konta</div>
        <div class="info">1 na godzinę</div>
      </div>
      <div class="limit">
        <div class="info">Aktualizacja konta</div>
        <div class="info">1 na godzinę</div>
      </div>
      <div class="limit" v-if="user.usertype === 2">
        <div class="info">Weryfikacja użytkownika</div>
        <div class="info">10 na godzinę</div>
      </div>
      <div class="limit" v-if="user.usertype === 2">
        <div class="info">Odświeżenie liczby prób użytkownika</div>
        <div class="info">10 na godzinę</div>
      </div>
      <div class="limit">
        <div class="info">Wykonanie predykcji</div>
        <div class="info" v-if="user.usertype === 0">10 na dzień</div>
        <div class="info" v-else-if="user.usertype === 1">30 na dzień</div>
        <div class="info" v-else>100 na dzień</div>
      </div>
      <div class="limit">
        <div class="info">Zmiana nazwy predykcji</div>
        <div class="info">50 na dzień</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.header-limit, .limit {
  width: 80%;
  height: 20%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
  border-radius: 0.75rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.7);
  margin: 1rem;
  padding: 1rem;
}

.info {
  width: 50%;
  text-align: center;
}

.go-main {
  width: 100%;
  height: 10%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  padding: 1rem 0 1rem 0;
}

.router-link {
  width: 10%;
  padding: 1rem;
}

li {
  list-style-type: '👉';
}

.header {
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
  font-size: 1.5vw;
}

.left-part {
  width: 90%;
  overflow-y: scroll;
  scrollbar-gutter: stable both-edges;
}

.limits {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

@media (max-width: 700px) {
  .header, .info {
    font-size: 1.5vh;
  }
}
</style>