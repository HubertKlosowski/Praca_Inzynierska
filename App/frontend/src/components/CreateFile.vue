<script setup>
import {onMounted, ref} from "vue";
import _ from "lodash";
import FormTextField from "@/components/FormTextField.vue";
import FormButtonField from "@/components/FormButtonField.vue";


const data = ref(JSON.parse(localStorage.getItem('to_file')))

const next_post = ref('')
const error = ref('')


const addPost = () => {
  if (next_post.value.length === 0) {
    error.value = 'Nie można dodać pustego wpisu.'
  } else if (_.includes(data.value, next_post.value)) {
    error.value = 'Dane nie mogą posiadać duplikatów.'
  } else {
    data.value.unshift(next_post.value)
    localStorage.setItem('to_file', JSON.stringify(data.value))
    localStorage.setItem('show_popup', JSON.stringify(data.value.length !== 0))
    next_post.value = ''
  }
}

const deletePost = (post) => {
  _.remove(data.value, function (p) {
    return p === post
  })
  localStorage.setItem('to_file', JSON.stringify(data.value))
  localStorage.setItem('show_popup', JSON.stringify(data.value.length !== 0))
}

onMounted(() => {
  if (data.value === null) {
    localStorage.setItem('to_file', JSON.stringify([]))
  }
  data.value = JSON.parse(localStorage.getItem('to_file'))
})
</script>

<template>
  <div class="left-part">
    <div class="header">
      <h3>Kreator pliku</h3>
      <ul>
        <li>Rozwiązuje problem z utworzeniem pliku.</li>
        <li>Podaj dowolną liczbę wpisów, a aplikacja sama stworzy plik za Ciebie.</li>
        <li>Wielkość pliku dla typ kont ciągle obowiązuje.</li>
        <li>Język musi być spójny dla każdego wpisu.</li>
      </ul>
    </div>
    <div class="main">
      <div class="form">
        <form @submit.prevent="addPost">

          <FormTextField
              v-model:input_value="next_post"
              :minimize="true"
              :label_info="''"
              :input_placeholder="'Wpis'"
              :label_name="''"
          ></FormTextField>

          <FormButtonField :login="true">
            <template v-slot:green>
              Dodaj
            </template>
          </FormButtonField>

        </form>
      </div>
      <div class="post" v-for="item in data" :key="item" v-if="data === null || data.length !== 0">
        <div class="field">
          {{ item }}
        </div>
        <button type="button" class="delete" @click="deletePost(item)">Usuń</button>
      </div>
      <div class="post" v-else>
        Brak wpisów
      </div>
    </div>
    <div class="buttons">
      <RouterLink to="/phases" class="router-link">Potwierdzam dane</RouterLink>
    </div>
  </div>
</template>

<style scoped>
.field {
  width: 50%;
  height: 90%;
  overflow-y: auto;
}

.delete {
  width: 20%;
  height: 70%;
  text-decoration: none;
  text-align: center;
  align-content: center;
  margin: 1rem;
  font-size: 1.5vw;
  transition: 0.4s ease;
  cursor: pointer;
  background-color: white;
  border-radius: 1rem;
  border: 2px solid red;
  color: red;
}

.delete:hover {
  color: white;
  border: 2px solid white;
  box-shadow: 0.5rem 0.5rem dodgerblue;
}

.delete:hover {
  background-color: darkred;
}

li {
  list-style-type: '👉';
}

.post {
  width: 90%;
  min-height: 20%;
  margin: 1rem 0 1rem 0;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
  background-color: #f5f5f5;
  border-radius: 0.75rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.7);
}

.form {
  width: 100%;
  height: 40%;
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
}

form {
  width: 100%;
  height: 100%;
  margin: 1rem;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.form-row {
  width: 40%;
  height: 40%;
}

.router-link {
  width: 20%;
  height: 50%;
}

.left-part {
  width: 90%;
}

.header, .buttons {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.header {
  width: 100%;
  height: 20%;
}

.main {
  width: 100%;
  height: 60%;
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
  overflow-y: auto;
}

.buttons {
  width: 100%;
  height: 20%;
}

@media (max-width: 700px) {
  .main, input[type="text"] {
    font-size: 1.5vh;
  }

  .header, button[type="button"] {
    font-size: 1.5vh;
  }

  .router-link {
    font-size: 1.5vh;
    width: 80%;
    height: 50%;
  }
}
</style>