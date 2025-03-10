<script setup>
import {inject, reactive} from "vue";
import _ from "lodash";


const $cookies = inject('$cookies')
const user = reactive(JSON.parse(localStorage.getItem('user')))


const check = () => {
  return (_.isEmpty(user) && !$cookies.isKey('made_submission')) || (!_.isEmpty(user))
}
</script>

<template>
  <div class="left-part">
    <div class="content">
      <h4>Informacje o predykcjach</h4>
      <p>Wyniki prezentują wykryty stopień depresji w zamieszczonych postach.</p>
      <p>W przypadku braku konta nie zostaną one zapisane w bazie danych.</p>
      <p>Jeśli chcesz posiadać możliwość powrotu do wcześniejszych wyników, zalecane jest utworzenie konta.</p>
      <p>Pozwoli ono pełny wgląd w historię predykcji.</p>
    </div>
    <div class="info">
      <div class="phase">
        <h4>Przygotuj dane</h4>
        <p>Analiza depresji wymaga posiadania danych w formacie tekstowym.</p>
        <p>Dane możesz wysłać w postaci pliku w rozszerzeniu "csv", "json" albo w formie pojedynczego wpisu.</p>
        <p>Każdy wpis powinien zostać umieszczony w osobnym wierszu.</p>
      </div>
      <div class="phase">
        <h4>Przeanalizuj wyniki</h4>
        <p>Każdy wpis zostanie poddany detekcji pod kątem występowania stanów depresyjnych.</p>
        <p>Osoby posiadające konto otrzymają dodatkowe statystyki.</p>
      </div>
    </div>
    <div class="links">
      <RouterLink
          to="/phases"
          class="router-link"
          v-if="check"
      >Sprawdź posty</RouterLink>
      <RouterLink
          to="/predict"
          class="router-link"
          v-if="$cookies.isKey('made_submission')"
      >Zobacz predykcje</RouterLink>
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

.info {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 1rem;
  justify-content: center;
  align-items: center;
  font-size: 1.5vw;
}

.phase {
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
  box-shadow: 0.5rem 0.5rem dodgerblue;
}

.phase h4 {
  margin-bottom: 0.5rem;
  font-size: 1.5vw;
  font-weight: bold;
}

.phase p {
  margin: 0.25rem 0;
}

@media (max-width: 700px) {
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