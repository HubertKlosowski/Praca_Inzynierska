<script setup>

</script>

<template>
  <div class="left-part">
    <div class="predict-content">
      <h3>Twoje predykcje</h3>
      <p>Predykcje wykonane jako gość nie będą zapisywane w bazie danych.</p>
      <p>Jeśli chcesz mieć możliwość powrotu do wyników w przyszłości, zalecane jest utworzenie konta.</p>
      <p>Pozwoli na pełny wgląd w historię predykcji.</p>
    </div>
    <div class="info">
      <div class="phase">
        <h3>Przygotuj dane</h3>
        <p>Analiza depresji wymaga posiadania danych tekstowych.</p>
        <p>Dane możesz wysłać w postaci pliku .csv lub w formie jednego wpisu.</p>
        <p>Każdy wpis powinien być umieszczony w osobnych wierszach.</p>
      </div>
      <div class="phase">
        <h3>Wybierz model</h3>
        <p>W tym etapie należy wybrać model wykonujący predykcje na przygotowanych danych.</p>
        <p>Są dostępne 2 modele, każdy w 2 wersjach:</p>
        <ul>
          <li>BERT BASE / LARGE (dla języka angielskiego)</li>
          <li>RoBERTa BASE / LARGE (dla języka polskiego)</li>
        </ul>
        <p>Wersja LARGE posiada lepszą dokładność, niż BASE &#128077;.</p>
        <p>Zaletą BASE jest szybszy czas wykonania &#128077;.</p>
      </div>
      <div class="phase">
        <h3>Przeanalizuj wyniki</h3>
        <p>Wyniki będą przypisane każdemu przesłanemu wpisowi.</p>
        <p></p>
      </div>
    </div>
    <div class="links">
      <RouterLink to="/phases" class="router-link">Przygotuj dane</RouterLink>
    </div>
  </div>
</template>

<style scoped>
@media (max-width: 768px) {
  .left-part {
    width: 90%;
    height: 45%;
    font-size: 1.5vh;
  }

  .left-part * {
    font-size: 1.5vh !important;
  }
}

.info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.phase {
  font-size: 1.25vw;
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
  box-shadow: 1rem 1rem mediumpurple;
}

ul {
  display: inline-block;
}
</style>