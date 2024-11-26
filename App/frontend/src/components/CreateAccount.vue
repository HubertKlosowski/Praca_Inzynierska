<script setup>
import {ref} from "vue";
import FormTextField from "@/components/FormTextField.vue";
import FormRadioField from "@/components/FormRadioField.vue";

const name = ref('')
const username = ref('')
const email = ref('')
const password = ref('')
const usertype = ref(0)

const createAccount = () => {
  let formData = new FormData()

  formData.append('name', name.value)
  formData.append('username', username.value)
  formData.append('email', email.value)
  formData.append('password', password.value)
  formData.append('usertype', usertype.value)

}

const resetInputs = () => {
  name.value = ''
  username.value = ''
  email.value = ''
  usertype.value = 0
}
</script>

<template>
  <div class="left-part">
    <div class="header">
      <h3>Utwórz konto</h3>
      <p>Poniżej znajduje się formularz, w którym należy podać własne dane osobowe. </p>
    </div>
    <div class="form">
      <form @submit.prevent="createAccount">

        <FormTextField
            :label_info="'Imie i nazwisko'"
            :label_name="'name'"
            @update_variable="(variable) => {name = variable}"></FormTextField>

        <FormTextField
            :label_info="'Nazwa użytkownika'"
            :label_name="'username'"
            @update_variable="(variable) => {username = variable}"></FormTextField>

        <FormTextField
            :label_info="'Email'"
            :label_name="'email'"
            @update_variable="(variable) => {email = variable}"></FormTextField>

        <FormTextField
            :label_info="'Hasło'"
            :label_name="'password'"
            @update_variable="(variable) => {password = variable}"></FormTextField>

        <FormRadioField @update_variable="(variable) => {usertype = variable}"></FormRadioField>

        <div class="buttons" style="border: none; height: 100px">
          <button type="submit" class="router-link">Wyślij</button>
          <button type="submit" class="router-link" @click="resetInputs()">Wyczyść</button>
        </div>
      </form>
    </div>
    <div class="buttons">
      <RouterLink to="/" class="router-link">Wróć do strony głównej</RouterLink>
    </div>
  </div>
</template>

<style scoped>
.header {
  height: 20%;
  width: 80%;
  padding: 1rem;
  margin: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  font-size: 2vw;
}

.left-part {
  width: 90%;
}

.form {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

form {
  border-top: 2px solid black;
  width: 100%;
  height: 100%;
  margin: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.buttons {
  border-top: 2px solid black;
  width: 100%;
  height: 20%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}

.buttons > * {
  font-size: 2vw;
}

@media (max-width: 900px) {
  .buttons > * {
    width: 100%;
  }

  .header {
    font-size: 2vh;
  }
}
</style>