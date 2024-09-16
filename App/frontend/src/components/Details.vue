<script setup>

</script>

<template>
  <div class="container">
    <h3>Ogólne informacje</h3>
    <p>Projekt dotyczy problemu depresji występującego coraz częściej w mediach społecznościowych. Stworzyłem tą aplikację
      dla osób chcących się dowiedzieć więcej na temat depresji. Dzięki zastosowaniu ostatnich osiągnięć z dziedziny uczenia
      głęgokiego (eng. Deep Learning) chce pomóc w walce z depresją. Użytkownik ma dostęp do modeli językowych, których celem
      jest wykrycie depresji w postach z popularnych portali (Reddit, X). Użytkowicy po przesłaniu pliku spełniającego
      kryteria, mają udostępnione następujące statystyki:
    </p>
    <ol type="1">
      <li>macierz pomyłek modelu</li>
      <li>wpływ poszczególnych słów w zdaniu/poście</li>
      <li>prawdopodobieństwa że dany post zawiera depresję, bądź nie</li>
    </ol>
    <h3>Wymagania dotyczące przesyłanych plików</h3>
    <ol>
      <li>rozszerzenie .csv</li>
      <li>mają zawierać 2 kolumny: text, label</li>
    </ol>
    <p>Projekt jest udostępniony na licencji MIT</p>
    <p>Link do Githuba: https://github.com/HubertKlosowski/Praca_Inzynierska</p>
  </div>
</template>

<style scoped>
.container {
  width: 80%;
  height: auto;
  align-items: flex-start;
  background-color: lightsteelblue;
  margin: 0 auto;
  padding: 10px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.9);
  color: #2c3e50;
  font-size: 1.2rem;
}
</style>