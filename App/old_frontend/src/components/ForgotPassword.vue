<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const email = ref('')

const resetPassword = () => {

}
</script>

<template>
  <div class="container">
    <form @submit.prevent="resetPassword">
      <label for="email">Podaj email do konta, na którym zapomniałeś/aś hasła</label>
      <input type="text" id="email" v-model="email">
      <div class="row">
        <RouterLink to="/" class="cancel">Anuluj</RouterLink>
        <button type="submit">Dalej</button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.container {
  width: 80%;
  padding: 20px;
  height: auto;
  margin: 0 auto;
  background-color: lightsteelblue;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
}

label {
  margin-top: 2%;
  margin-bottom: 4%;
  font-weight: bold;
  color: #2c3e50;
}

form {
  display: flex;
  flex-direction: column;
  width: 45%;
  height: 40%;
  padding: 20px;
  background-color: rgb(248, 249, 250);
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

input[type="text"] {
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  font-size: 1rem;
  background-color: #ecf0f1;
  transition: border-color 0.3s;
}

.row {
  padding: 10px;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
}

button[type="submit"], .cancel {
  padding: 10px 15px;
  width: 45%;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

button[type="submit"] {
  background-color: forestgreen;
}

.cancel {
  background-color: lightslategrey;
  text-decoration: none;
  text-align: center;
}

.cancel:hover {
  background-color: darkslategrey;
}

button[type="submit"]:hover {
  background-color: darkgreen;
}
</style>