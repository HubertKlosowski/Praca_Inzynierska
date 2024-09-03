<script setup>

</script>

<template>
  <div class="submission">
    <div class="submit">

    </div>
    <div class="choose_model">

    </div>
    <div class="stats">

    </div>
  </div>
</template>

<style scoped>
.submission {
  width: 80%;
  padding: 20px;
  height: 90%;
  margin: 0 auto;
  background-color: lightsteelblue;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
}

.submit, .choose_model, .stats {
  height: 42%;
  background-color: rgb(248, 249, 250);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.submit {
  width: 45%;
}

.choose_model {
  width: 45%;
}

.stats {
  width: 100%;
}
</style>