<script setup>

</script>

<template>
  <div class="left-part">
    <h3>Informacje o koncie</h3>
    <p>Utworzenie konta umożliwia uzyskanie dostępu do nowych możliwości:</p>
    <ol class="list">
      <li>zapisanie wyników twoich analiz</li>
      <li>rozbudowanie o ogólne statystyki dla wszystkich wpisów</li>
      <li>wykorzystanie dodatkowych cech w określeniu depresji</li>
    </ol>
    <p>Korzystanie z konta jest proste, oraz w pełni przejrzyste &#128522;.</p>
    <p>Poniżej znajdują się trzy dostępne typy kont:</p>
    <div class="types-accounts">
      <div class="account">
        <h4>Standard</h4>
        <ul>
          <li>liczba dziennych prób: 10</li>
          <li>analiza pojedyńczych wpisów</li>
          <li>max. wielkość pliku: do 20KB</li>
        </ul>
      </div>
      <div class="account">
        <h4>Pro</h4>
        <ul>
          <li>liczba dziennych prób: 30</li>
          <li>ogólne statystyki dla plików</li>
          <li>max. wielkość pliku: do 100KB</li>
        </ul>
      </div>
      <div class="account">
        <h4>Admin</h4>
        <ul>
          <li>liczba dziennych prób: 100</li>
          <li>wykresy dotyczące danych</li>
          <li>max. wielkość pliku: do 1 000KB</li>
        </ul>
      </div>
    </div>
    <div class="links">
      <RouterLink to="/create_account" class="router-link">Utwórz konto</RouterLink>
      <RouterLink to="/login" class="router-link">Zaloguj się</RouterLink>
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

.types-accounts {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 1rem;
  justify-items: center;
  font-size: 1.25vw;
  box-sizing: border-box;
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
  box-shadow: 1rem 1rem mediumpurple;
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
</style>