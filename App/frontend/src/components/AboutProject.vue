<script setup>

</script>

<template>
  <div class="left-part">
    <h3>Witaj w aplikacji pracy inżynierskiej</h3>
    <p>Aplikacja została stworzona z myślą o wsparciu osób dotkniętych zaburzeniami depresyjnymi.</p>
    <p>Jej główną funkcją jest wykorzystanie modeli językowych do wykrywania oznak depresji na podstawie wpisów w social mediach.</p>
    <p>Dodatkowo użytkownik otrzyma informacje zwrotne o ogólnym stanie na podstawie analizy poszczególnych postów.</p>
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
</style>