<script setup>
import { ref } from 'vue'
import AdminPanel from '@/components/AdminPanel.vue'
import UserPanel from '@/components/UserPanel.vue'

const manage_users = ref(false)
</script>

<template>
  <UserPanel
      @go-back="manage_users = true"
      v-if="!manage_users"
  ></UserPanel>
  <AdminPanel
      @go-back="manage_users = false"
      v-else
  ></AdminPanel>
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
  justify-content: space-evenly;
}
</style>