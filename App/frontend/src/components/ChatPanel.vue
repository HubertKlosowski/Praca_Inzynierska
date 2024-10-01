<script setup>
import { ref, inject, onMounted } from 'vue'
import axios from 'axios'

const $cookies = inject('$cookies')

const question = ref('')

const createMyDiv = (textValue, backgroundColor) => {
  const element = document.createElement('div')
  element.style.width = '80%'
  element.style.height = '10%'
  element.style.margin = '10px'
  element.style.padding = '10px'
  element.style.borderRadius = '10px'
  element.style.backgroundColor = backgroundColor
  element.style.color = '#2c3e50'
  element.textContent = textValue
  return element
}

const sendMessage = async () => {
  if (question.value.length !== 0) {
    const chatHistory = $cookies.get('chat')
    const q_and_a = {
      'sent_at': new Date().toISOString(),
      'question': question.value,
      'answer': ''
    }
    try {
      const response = await axios.post('http://localhost:8000/api/user/get_answer', q_and_a)
      q_and_a['answer'] = response.data['answer']
    } catch (error) {
      const error_response = error.response.data
      q_and_a['answer'] = error_response['answer']
    }
    chatHistory.push(q_and_a)
    $cookies.set('chat', chatHistory)

    const parentElement = document.getElementsByClassName('main_chat')[0]
    parentElement.append(createMyDiv(q_and_a['question'], 'lightsteelblue'))
    parentElement.append(createMyDiv(q_and_a['answer'], 'lightblue'))
    question.value = ''
  }
}

onMounted(() => {
  if (!$cookies.isKey('chat')) {
    $cookies.set('chat', [])
  }

  const parentElement = document.getElementsByClassName('main_chat')[0]
  for (const message of $cookies.get('chat')) {
    parentElement.append(createMyDiv(message['question'], 'lightsteelblue'))
    parentElement.append(createMyDiv(message['answer'], 'lightblue'))
  }
})
</script>

<template>
  <div class="chat">
    <div class="main_chat"></div>
    <div class="message">
      <input type="text" id="question" v-model="question" placeholder="Wyślij wiadomość">
      <div class="button">
        <img src="@/assets/send.png" alt="Wyślij" @click="sendMessage">
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat {
  width: 90%;
  height: 100vh;
  background-color: rgb(248, 249, 250);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  color: #2c3e50;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}

.main_chat {
  width: 100%;
  height: 80%;
  display: flex;
  flex-direction: column;
  max-height: 80%;
  overflow-y: auto;
}

.message {
  width: 100%;
  height: 10%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}

input {
  width: 85%;
  height: 50%;
  padding: 10px 15px;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  font-size: 1rem;
  background-color: #ecf0f1;
  transition: border-color 0.3s;
}

.button {
  width: 15%;
  height: 100%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

img {
  width: 40%;
  height: auto;
  cursor: pointer;
}
</style>