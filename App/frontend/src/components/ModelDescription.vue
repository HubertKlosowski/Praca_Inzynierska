<script setup>

</script>

<template>
  <div class="main">
    <div class="phases">
      <h3>Etapy konfiguracji modelu:</h3>
      <ul>
        <li>Wstęp</li>
        <li>Wybór wersji językowej</li>
        <li>Wybór wersja modelu</li>
        <li>Zatwierdzenie</li>
      </ul>
    </div>
    <div class="phases-description">
      <h3>Opis:</h3>
      <p>Przed przejściem do kolejnego etapu zostanie wyświetlony jego krótki opis.</p>
      <p>W nagłówku wyświetlane jest twoje położenie na stronie.
        Koło oznaczone na czerwono wskazuje obecnie wyświetlany etap.</p>
      <p>Ikonka znaku zapytania umożliwia powrót od opisu, jeśli istnieje taka potrzeba.</p>
      <p>W trakcie przechodzenia przez etapy musisz wybrać elementy konfiguracji swojego modelu.</p>
      <p>Twoje wybory zostaną przedstawione w ostatnim etapie.</p>
    </div>
  </div>
</template>

<style scoped>
.main {
  width: 100%;
  height: 80%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}

@media (max-width: 768px) {
  .main {
    flex-direction: column;
    font-size: 1.75vh;
  }

  .main * {
    font-size: 1.75vh !important;
  }

  .phases, .phases-description {
    width: 80% !important;
    height: 50%;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
  }

  .phases {
    overflow-y: hidden;
  }

  .phases-description {
    overflow-y: auto;
  }
}

.phases, .phases-description {
  width: 40%;
  height: 80%;
  background-color: #f5f5f5;
  border-radius: 0.75rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.5rem;
  overflow-y: auto;
}
</style>