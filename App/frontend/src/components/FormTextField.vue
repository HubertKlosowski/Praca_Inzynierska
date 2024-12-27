<script setup>
const props = defineProps(['label_info', 'input_placeholder', 'label_name', 'reset', 'error', 'minimize'])
const input_value = defineModel('input_value')
const show_password = defineModel('show_password')
</script>

<template>
  <div class="form-row">
    <div class="row" v-if="!minimize">
      <label :for="props.label_name">Podaj {{ props.label_info.toLowerCase() }}</label>
    </div>
    <div class="just-row" :style="{
      width: !minimize ? '60%' : '90%'
    }">
      <input
        v-model="input_value"
        type="text"
        :id="props.label_name"
        :placeholder="props.input_placeholder"
        :style="{
          width: show_password ? '90%' : '100%'
        }"
        v-if="show_password === undefined || show_password"
      />
      <input
        v-model="input_value"
        type="password"
        :id="props.label_name"
        :placeholder="props.input_placeholder"
        v-else
      />
      <div
          class="show"
          :style="{
            display: show_password !== undefined ? 'initial' : 'none'
          }">
        <font-awesome-icon
          :icon="['fas', 'eye']"
          v-if="show_password"
          @click="show_password = !show_password" />
        <font-awesome-icon
          :icon="['fas', 'eye-slash']"
          v-else
          @click="show_password = !show_password" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.just-row {
  width: 60%;
  height: 90%;
  display: flex;
  flex-direction: row;
}

.show {
  width: 10%;
  min-height: 2rem;
  border-radius: 0.75rem;
  border: 2px solid black;
}

svg {
  width: 100%;
  height: 100%;
}

.form-row {
  width: 80%;
  height: 20%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
  border-radius: 0.75rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.7);
  margin: 1rem;
  padding: 1rem;
}

.row {
  width: 40%;
  height: 90%;
  font-size: 1.5vw;
  padding: 1rem;
  display: flex;
  flex-direction: row;
  align-items: center;
}

input[type="text"], input[type="password"] {
  width: 90%;
  min-height: 2rem;
  font-size: 1.5vw;
  box-sizing: border-box;
  padding: 1rem;
  border-radius: 0.75rem;
}

@media (max-width: 700px) {
  .form-row {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .just-row {
    width: 100%;
    height: 90%;
  }

  input[type="text"], input[type="password"] {
    height: 70%;
    width: 100%;
    font-size: 1.5vh;
  }

  .show {
    width: 20%;
    height: 70%;
    border-radius: 0.75rem;
  }

  .row {
    display: none;
  }
}
</style>
