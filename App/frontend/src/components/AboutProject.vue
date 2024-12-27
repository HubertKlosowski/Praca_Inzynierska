<script setup>

</script>

<template>
  <div class="left-part">
    <h3>Witaj w aplikacji eDepresja</h3>
    <p>Aplikacja została stworzona z myślą o wsparciu osób dotkniętych zaburzeniami depresyjnymi.</p>
    <p>Jej główną funkcją jest wykorzystanie modeli językowych do wykrywania depresji na podstawie wpisów w mediach społecznościowych.</p>
    <p>Każdy użytkownik otrzyma informacje zwrotne na podstawie analizy poszczególnych postów.</p>
    <p>Szczegółowe informacje dotyczące możliwości aplikacji można znaleźć w kartach "Twoje konto" i "Sprawdź posty".</p>
  </div>
</template>

<style scoped>
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