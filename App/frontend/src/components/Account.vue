<script setup>
import {inject, onMounted, ref, watch} from "vue";
import polish from "@/assets/polski.png";
import english from "@/assets/angielski.png";
import {useRouter} from "vue-router";

const router = useRouter()
const $cookies = inject('$cookies')

const user = ref($cookies.get('user'))
const usertypes = ['Normal', 'Pro', 'Administrator']

const go = ref(0)
const choose_polish = ref(false)
const choose_english = ref(false)
const submissions = ref(JSON.parse(localStorage.getItem('submissions')))
const users_verify = ref([])
const models = ref(['roberta-base', 'bert-base'])

const logoutUser = async () => {
  if (user.value['usertype'] === 2)
    localStorage.removeItem('users_verify')
  $cookies.remove('user')
  localStorage.removeItem('submissions')
  await router.push('/')
}

const showDetails = () => {

}

const setPolishModel = () => {
  choose_polish.value = !choose_polish.value
  models.value[0] = choose_polish.value ? 'roberta-large' : 'roberta-base'
  localStorage.setItem('choosen_models', JSON.stringify(models.value))
}

const setEnglishModel = () => {
  choose_english.value = !choose_english.value
  models.value[1] = choose_english.value ? 'bert-large' : 'bert-base'
  localStorage.setItem('choosen_models', JSON.stringify(models.value))
  console.log(JSON.parse(localStorage.getItem('choosen_models')))
}

onMounted(() => {
  if (user.value['usertype'] === 2) {
    users_verify.value = JSON.parse(localStorage.getItem('users_verify'))
  } else {
    users_verify.value = []
  }

  if (JSON.parse(localStorage.getItem('choosen_models')) === null) {
    localStorage.setItem('choosen_models', JSON.stringify(models.value))
  } else {
    console.log(JSON.parse(localStorage.getItem('choosen_models')))
    models.value = JSON.parse(localStorage.getItem('choosen_models'))
    choose_polish.value = models.value[0] !== 'roberta-base'
    choose_english.value = models.value[1] !== 'bert-base'
  }
})
</script>

<template>
  <div class="left-part">
    <div class="header">
      <h3>Witaj {{ user['username'] }}!</h3>
      <div class="info">{{ user['name'] }}</div>
      <div class="info">{{ user['email'] }}</div>
      <div class="info">{{ usertypes[user['usertype']] }}</div>
      <div class="info">{{ user['submission_num'] }}</div>
      <button type="button" class="logout" @click="logoutUser()">Wyloguj się</button>
    </div>
    <div class="model-config">
      <h3>Konfiguracja modelu</h3>
      <div class="models">
        <h3>LARGE</h3>
        <div class="t-buttons">
          <div
              class="toggle-button"
              :style="{ justifyContent: choose_polish ? 'start' : 'end' }"
              @click="setPolishModel()">
            <div class="circle" :style="{
              backgroundImage: `url(${polish})`,
              backgroundRepeat: 'no-repeat',
              backgroundSize: 'cover',
              backgroundPosition: 'center'
            }"></div>
          </div>
          <div
              class="toggle-button"
              :style="{ justifyContent: choose_english ? 'start' : 'end' }"
              @click="setEnglishModel()">
            <div class="circle" :style="{
              backgroundImage: `url(${english})`,
              backgroundRepeat: 'no-repeat',
              backgroundSize: 'cover',
              backgroundPosition: 'center'
            }"></div>
          </div>
        </div>
        <h3>BASE</h3>
      </div>
    </div>
    <div class="history">
      <h3>Historia predykcji</h3>
      <div class="h-submissions">
        <div class="history-submission" v-for="(item, i) in submissions" :key="i">
          <div class="field" v-if="item.name !== null">{{ item.name }}</div>
          <div class="field" v-if="item.name === null">Brak nazwy</div>
          <div class="field">
            <button type="button" class="details" @click="showDetails">Pokaż szczegóły</button>
          </div>
        </div>
      </div>
    </div>
    <div class="verify" v-if="$cookies.get('user')['usertype'] === 2">
      <h3>Użytkownicy do zweryfikowania</h3>
      <div class="u-verify">
        <div class="user-verify" v-for="(item, i) in users_verify" :key="i">
          <div class="field" v-for="(el, j) in item" :key="j">
            <span v-if="j !== 'usertype'">{{ el }}</span>
            <span v-else>{{ usertypes[el] }}</span>
          </div>
        </div>
      </div>
    </div>
    <div class="buttons">
      <button type="button" @click="go = 1" class="update">Zmień dane</button>
      <button type="button" @click="go = 2" class="delete">Usuń konto</button>
      <RouterLink to="/" class="router-link">Wróć do strony głównej</RouterLink>
    </div>
  </div>
</template>

<style scoped>
.history, .verify {
  border-top: 2px solid black;
  height: 60%;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow-y: auto;
}

.h-submissions, .u-verify {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
  overflow-y: auto;
}

.history-submission, .user-verify {
  width: 90%;
  min-height: 40%;
  margin: 1rem 0 1rem 0;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
  background-color: #f5f5f5;
  border-radius: 0.75rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.7);
}

.field {
  width: 40%;
  height: 80%;
  font-size: 1.5vw;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.model-config {
  border-top: 2px solid black;
  height: 40%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}

.models {
  width: 50%;
  height: 90%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}

.t-buttons {
  width: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.toggle-button {
  width: 80%;
  margin: 0.5rem;
  background-color: gray;
  border-radius: 4vw;
  display: flex;
  flex-direction: row;
  align-items: center;
}

.circle {
  width: 4vw;
  height: 4vw;
  border-radius: 50%;
  border: 2px solid black;
  transition: transform 0.3s ease;
}

.logout {
  width: 10%;
  height: 60%;
}

.details {
  width: 80%;
  height: 60%;
}

.update, .delete {
  width: 30%;
  height: 60%;
}

.update, .delete, .logout, .details {
  text-decoration: none;
  text-align: center;
  align-content: center;
  margin: 1rem;
  font-size: 1.35vw;
  transition: 0.4s ease;
  cursor: pointer;
  background-color: white;
  border-radius: 1rem;
}

.update:hover, .delete:hover, .logout:hover, .details:hover {
  color: white;
  border: 2px solid white;
  box-shadow: 1rem 1rem dodgerblue;
}

.update:hover {
  background-color: darkgreen;
}

.delete:hover {
  background-color: darkred;
}

.logout:hover, .details:hover {
  background-color: darkgrey;
}

.update {
  border: 2px solid green;
  color: green;
}

.delete {
  border: 2px solid red;
  color: red;
}

.logout, .details {
  border: 2px solid black;
  color: black;
}

.left-part {
  width: 90%;
  overflow-y: auto;
}

.header {
  height: 20%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}

.buttons {
  border-top: 2px solid black;
  height: 20%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

@media (max-width: 768px) {
  .buttons {
    display: flex;
    flex-direction: column;
    height: 40%;
  }

  .buttons > * {
    width: 60%;
    height: 30%;
    font-size: 2vh;
  }

  .field {
    width: 80%;
    height: 40%;
  }

  .circle {
    width: 4vh;
    height: 4vh;
    border-radius: 50%;
    border: 2px solid black;
  }

  .model-config, .header, .user-verify {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .model-config, .header {
    overflow-y: auto;
  }

  .toggle-button {
    height: 30%;
  }

  .models {
    width: 90%;
    height: auto;
  }

  h3, .field, .details, .logout {
    font-size: 1.5vh;
  }

  .info {
    font-size: 1.25vh;
  }

  .logout {
    width: 60%;
    height: 30%;
  }
}
</style>