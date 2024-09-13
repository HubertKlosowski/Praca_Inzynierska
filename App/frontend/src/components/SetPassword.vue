<script setup>
import { ref, watch } from 'vue'

const show_password = ref(false)
const password = ref('')

const emit = defineEmits(['setPassword'])

watch(password, (passwd) => {
  emit('setPassword', passwd)
})

window.addEventListener('copy', event => event.preventDefault())
</script>

<template>
  <label for="password">Hasło</label>
  <div class="password_part">
    <input v-if="!show_password" type="password" id="password" v-model="password">
    <input v-else type="text" id="password" v-model="password">
    <button type="button" @click="show_password = !show_password">
      <i class="fas" :class="{ 'fa-eye-slash': !show_password, 'fa-eye': show_password }"></i>
    </button>
  </div>
</template>

<style scoped>
label {
  margin-bottom: 4px;
  font-weight: bold;
  color: #2c3e50;
}

.password_part {
  display: flex;
  flex-direction: row;
}

input[type="text"], input[type="password"], button[type="button"] {
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  font-size: 1rem;
  background-color: #ecf0f1;
  transition: border-color 0.3s;
}

#password {
  width: 85%;
}

button[type="button"] {
  width: 15%;
}
</style>