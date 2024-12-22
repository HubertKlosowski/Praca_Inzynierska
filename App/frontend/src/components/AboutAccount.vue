<script setup>
import {ref} from "vue";
import _ from "lodash";


const user = ref(JSON.parse(localStorage.getItem('user')))
</script>

<template>
  <div class="left-part">
    <div class="content">
      <h4>Informacje o koncie</h4>
      <p>Utworzenie konta umożliwia uzyskanie dostępu do nowych możliwości:</p>
      <ol class="list">
        <li>zapisanie wyników twoich analiz</li>
        <li>udostępnienie ogólnych statystyk i wykresów do wyników</li>
        <li>kreator plików w przypadku problemów z ich stworzeniem</li>
      </ol>
      <p>Korzystanie z konta jest proste i przejrzyste &#128522;.</p>
      <p>Poniżej znajdują się trzy dostępne typy kont:</p>
    </div>
    <div class="types-accounts">
      <div class="account">
        <h4>Standard</h4>
        <ul>
          <li>liczba dziennych prób: 10</li>
          <li>analiza pojedyńczych wpisów</li>
          <li>max. wielkość pliku: do 200KB</li>
        </ul>
      </div>
      <div class="account">
        <h4>Pro</h4>
        <ul>
          <li>liczba dziennych prób: 30</li>
          <li>ogólne statystyki dla plików</li>
          <li>max. wielkość pliku: do 1MB</li>
        </ul>
      </div>
      <div class="account">
        <h4>Admin</h4>
        <ul>
          <li>liczba dziennych prób: 100</li>
          <li>wykresy dotyczące danych</li>
          <li>max. wielkość pliku: do 10MB</li>
        </ul>
      </div>
    </div>
    <div class="links">
      <RouterLink to="/create_account" class="router-link" v-if="_.isEmpty(user)">Utwórz konto</RouterLink>
      <RouterLink to="/login" class="router-link" v-if="_.isEmpty(user)">Zaloguj się</RouterLink>
      <RouterLink to="/profile" class="router-link" v-else>Twoje konto</RouterLink>
    </div>
  </div>
</template>

<style scoped>
.content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.router-link {
  width: 50%;
  height: 70%;
}

.types-accounts {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 1rem;
  justify-content: center;
  align-items: center;
  font-size: 1.5vw;
}

.account {
  width: 90%;
  padding: 1rem;
  background-color: #FFDAB9;
  color: black;
  border-radius: 1rem;
  text-align: center;
  transition: 0.4s ease;
  border: 2px solid black;
}

.account:hover {
  color: black;
  border: 2px solid white;
  background-color: #FF8C00;
  box-shadow: 0.5rem 0.5rem dodgerblue;
}

.account h4 {
  margin-bottom: 0.5rem;
  font-size: 1.5vw;
  font-weight: bold;
}

.account p {
  margin: 0.25rem 0;
}

ul {
  display: inline-block;
}

li {
  font-size: 1.5vw;
}

@media (max-width: 768px) {
  .left-part {
    width: 90%;
    height: 45%;
    font-size: 1.75vh;
  }

  .left-part * {
    font-size: 1.75vh !important;
  }
}
</style>