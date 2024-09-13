<script setup>

</script>

<template>
  <div class="main">
    <div class="row">
      <div class="question">
        Czym jest depresja?
      </div>
      <div class="content">
        <b>Zaburzenie depresyjne</b> jest częstym zaburzeniem psychicznym. Obejmuje obniżoną lub utratę przyjemności z wykonywanych czynności.
        Depresja różni się od zwykłych zmian nastroju i uczuć związanych z codziennym życiem.
        Osoba poddana temu zaburzeniu odczuwa nastrój depresyjny <b>(smutek, szybko się irytuje, czuje wewnątrzną pustkę)</b>.
        Traci satysfakcję, chęci z wykonywanych wcześniej codziennych czynności.
        Około <b>280</b> milionów osób zmaga się z depresją. Ponad <b>700</b> tysięcy osób popełnia samobójstwo.
      </div>
    </div>
    <div class="row">
      <div class="content">
        <ul class="symptoms">
          <li>słaba koncentracja</li>
          <li>uczucie przygnębienia i niskiej samooceny</li>
          <li>myślenie o samobójstwie, śmierci</li>
          <li>zakłocony sen</li>
          <li>brak energii i uczucie zmęczenia</li>
          <li>utrata apetytu lub wagi</li>
        </ul>
      </div>
      <div class="question">
        Jakie są objawy depresji?
      </div>
    </div>
    <div class="row">
      <div class="question">
        Jak leczy się depresję?
      </div>
      <div class="content">
        Według WHO: <i>Istnieją skuteczne metody leczenia depresji.
        Obejmują one terapię psychologiczną oraz leki.
        Zasięgnij pomocy, jeśli masz objawy depresji.
        Terapia psychologiczna jest pierwszą metodą leczenia depresji.
        Może być łączona z lekami przeciwdepresyjnymi w przypadku umiarkowanej i ciężkiej depresji.
        Leki przeciwdepresyjne nie są potrzebne w przypadku łagodnej depresji.</i>
      </div>
    </div>
    <div class="row">
      <div class="content">
        <ul class="goals">
          <li>Walka z depresją</li>
          <li>Zwiększenie świadomości o problemie depresji w mediach społecznościowych</li>
          <li>Pomoc społeczności polskiej</li>
        </ul>
      </div>
      <div class="question">
        Cele aplikacji
      </div>
    </div>
    <div class="row">
      <div class="question">
        Możliwości aplikacji
      </div>
      <div class="content">
        <ul class="features">
          <li>Możliwość detekcji depresji we wpisach użytkowników</li>
          <li>Obsługa angielskich i polskich wpisów</li>
          <li>Wykorzystanie LLM's do wykrycia depresji</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.main {
  flex: 3;
  background-color: steelblue;
  color: white;
  padding: 20px;
  display: flex;
  flex-direction: column;
  max-height: 64vh;
  overflow-y: auto;
}

.row {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: space-evenly;
  align-items: center;
  color: #2c3e50;
  padding: 10px;
}

.question {
  width: 45%;
  height: 250px;
  justify-content: center;
  align-content: center;
  background-color: rgb(248, 249, 250);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-size: 3rem;
}

.content {
  width: 45%;
  height: 500px;
  justify-content: center;
  align-content: center;
  background-color: rgb(248, 249, 250);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-size: 1.5rem;
}

.symptoms > * {
  list-style-type: "😞";
}

.goals > *, .features > * {
  list-style-type: "✅";
}
</style>