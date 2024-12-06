<script setup>
import {inject, ref} from "vue";

const $cookies = inject('$cookies')
const user = ref(JSON.parse(localStorage.getItem('user')))

const checkUser = () => {
  return !(user === null && $cookies.isKey('made_submission'))
}
</script>

<template>
  <div class="left-part">
    <div class="predict-content">
      <h3>Twoje wyniki</h3>
      <p>Wyniki przedstawią wykryte stopnie depresji w przekazanych danych.</p>
      <p>Bez konta nie będą zapisywane w bazie danych uzyskane wyniki.</p>
      <p>Jeśli chcesz mieć możliwość powrotu do wcześniejszych wyników w przyszłości, zalecane jest utworzenie konta.</p>
      <p>Pozwoli na pełny wgląd w historię predykcji.</p>
    </div>
    <div class="info">
      <div class="phase">
        <h3>Przygotuj dane</h3>
        <p>Analiza depresji wymaga posiadania danych tekstowych.</p>
        <p>Dane możesz wysłać w postaci pliku w rozszerzeniu "csv", "json" lub w formie pojedyńczego wpisu.</p>
        <p>Każdy wpis powinien być umieszczony w osobnych wierszach.</p>
      </div>
      <div class="phase">
        <h3>Przeanalizuj wyniki</h3>
        <p>Wyniki będą przypisane każdemu przesłanemu wpisowi.</p>
        <p>Dodatkowo, osoby posiadające konto otrzymają rozbudowane wyniki</p>
      </div>
    </div>
    <div class="links">
      <RouterLink to="/phases" class="router-link" v-if="checkUser">Sprawdź posty</RouterLink>
      <RouterLink to="/predict" class="router-link" v-if="$cookies.isKey('made_submission')">Zobacz predykcje</RouterLink>
    </div>
  </div>
</template>

<style scoped>
.router-link {
  width: 50%;
}

.info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.phase {
  font-size: 1.5vw;
  width: 90%;
  padding: 1rem;
  background-color: #FFDAB9;
  color: black;
  border-radius: 1rem;
  text-align: center;
  transition: 0.4s ease;
  border: 2px solid black;
}

.phase:hover {
  color: black;
  border: 2px solid white;
  background-color: #FF8C00;
  box-shadow: 1rem 1rem dodgerblue;
}

ul {
  display: inline-block;
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