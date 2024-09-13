<script setup>
import { ref } from 'vue'
import ChatPanel from '@/components/ChatPanel.vue'
import StatsPanel from '@/components/StatsPanel.vue'
import SubmitPanel from '@/components/SubmitPanel.vue'

const show = ref(-1)
</script>

<template>
  <div class="submission">
    <SubmitPanel
        @show-component="(param) => show = param"
        :style="{ maxHeight: show === 1 ? '90%' : '1%',
        display: show !== 1 && show !== -1 ? 'none': 'initial' }"></SubmitPanel>
    <ChatPanel
        @show-component="(param) => show = param"
        :style="{ maxHeight: show === 2 ? '90%' : '1%',
        display: show !== 2 && show !== -1 ? 'none': 'initial' }"></ChatPanel>
    <StatsPanel
        @show-component="(param) => show = param"
        :style="{ maxHeight: show === 3 ? '90%' : '1%',
        display: show !== 3 && show !== -1 ? 'none': 'initial' }"></StatsPanel>
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
</style>