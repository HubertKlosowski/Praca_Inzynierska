<script setup>
import { inject } from 'vue'

const $cookies = inject('$cookies')
</script>

<template>
  <div class="submission">
    <RouterView></RouterView>
    <div class="row">
      <RouterLink
          to="/submissions/submit"
          class="additional_links"
      >
        Sprawdź plik
      </RouterLink>
      <RouterLink
          to="/submissions/chat"
          class="additional_links"
          v-show="$cookies.get('user')['usertype'] !== 0"
      >
        Rozpocznij chat
      </RouterLink>
      <RouterLink
        to="/submissions/stats"
        class="additional_links"
      >
        Zobacz statystyki
      </RouterLink>
    </div>
  </div>
</template>

<style scoped>
.submission {
  width: 90%;
  padding: 20px;
  height: 90%;
  margin: 0 auto;
  background-color: lightsteelblue;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-evenly;
}

.row {
  width: 100%;
  height: 10%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-evenly;
}

.additional_links {
  margin-top: 20px;
  color: blue;
  font-size: 1.2rem;
  text-decoration: none;
  padding: 20px;
  transition: color 0.3s ease;
  background-color: rgb(248, 249, 250);
  border-radius: 8px;
  text-align: center;
}

.additional_links:hover {
  color: darkblue;
}
</style>