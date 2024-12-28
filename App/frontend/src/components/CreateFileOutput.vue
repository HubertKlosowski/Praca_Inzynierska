<script setup>
const show_popup = defineModel('show_popup')
const send_creator = defineModel('send_creator')

const deleteCreator = () => {
  localStorage.removeItem('to_file')
  localStorage.removeItem('show_popup')
  show_popup.value = false
  send_creator.value = false
}

const sendCreator = () => {
  localStorage.removeItem('show_popup')
  show_popup.value = false
  send_creator.value = true
}
</script>

<template>
  <div class="pop-up">
    <div class="header">
      <h3>Wykryto dane z kreatora</h3>
    </div>
    <div class="content">
      <p>Zostały dodane wpisy do kreatora.</p>
      <p>Co z nimi zrobić?</p>
      <div class="buttons">
        <button type="button" @click="sendCreator" class="router-link">Wyślij</button>
        <button type="button" @click="deleteCreator" class="delete">Usuń</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.router-link {
  width: 20%;
  height: 70%;
}

.delete {
  width: 20%;
  height: 70%;
  text-decoration: none;
  text-align: center;
  align-content: center;
  margin: 1rem;
  font-size: 1.25vw;
  transition: 0.4s ease;
  cursor: pointer;
  background-color: white;
  border-radius: 1rem;
}

.delete {
  border: 2px solid red;
  color: red;
}

.delete:hover {
  color: white;
  border: 2px solid white;
  box-shadow: 0.5rem 0.5rem dodgerblue;
  background-color: darkred;
}

.buttons {
  border-top: 2px solid black;
  height: 50%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.pop-up {
  position: fixed;
  top: 20%;
  width: 90%;
  height: 70%;
  padding: 2rem;
  background-color: rgba(245, 245, 245, 0.95);
  border-radius: 1rem;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  color: #333;
  animation: slide-down 0.7s ease-in;
}

@keyframes slide-down {
  0% {
    transform: translateY(-60%);
    opacity: 0;
  }
  100% {
    transform: translateY(0%);
    opacity: 1;
  }
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  border-bottom: 1px solid #ccc;
  padding-bottom: 0.5rem;
  height: 20%;
}

.header h3 {
  font-size: 1.5vw;
  margin: 0;
  color: black;
}

.content {
  text-align: left;
  background-color: #f5f5f5;
  padding: 1rem;
  border-radius: 0.5rem;
  height: 60%;
}

.content h4 {
  font-size: 1vw;
  margin: 0 0 1rem 0;
  color: #333;
}

.content ul {
  list-style-type: disc;
  margin: 0;
  padding-left: 1.5rem;
}

.content li {
  font-size: 1vw;
  color: #333;
  margin-bottom: 0.5rem;
}

@media (max-width: 700px) {
  .buttons {
    display: flex;
    flex-direction: column;
  }

  .router-link {
    width: 70%;
  }

  .pop-up {
    padding: 1.5rem;
    font-size: 1.75vh;
  }

  .delete {
    font-size: 1.75vh;
    width: 70%;
  }

  .header h3 {
    font-size: 1.75vh;
  }

  .content h4 {
    font-size: 1.5vh;
  }

  .content li {
    font-size: 1.5vh;
  }
}
</style>