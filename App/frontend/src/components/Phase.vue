<script setup>
import {onMounted, onUpdated, ref} from "vue";
import PhaseIntro from "@/components/PhaseIntro.vue";
import ModelDescription from "@/components/ModelDescription.vue";
import ModelLanguage from "@/components/ModelLanguage.vue";
import ModelVersion from "@/components/ModelVersion.vue";
import ModelOverview from "@/components/ModelOverview.vue";
import PrepareData from "@/components/PrepareData.vue";

const props = defineProps(['phase', 'num_phase'])

const show_intro = ref(true)
const current = ref(0)

const moveForward = () => {
  return props.num_phase === 5 || current.value < props.num_phase
}

onUpdated(() => {
  if (show_intro.value) {
    const magic = document.querySelector('.magic')
    magic.removeEventListener('animationend', () => { show_intro.value = false })
    magic.addEventListener('animationend', () => { show_intro.value = false })
  }
})

onMounted(() => {
  const magic = document.querySelector('.magic')
  magic.addEventListener('animationend', () => { show_intro.value = false })
})
</script>

<template>
  <PhaseIntro v-if="show_intro" :phase="props.phase"></PhaseIntro>
  <div class="model" v-else :style="{height: props.num_phase === 4 ? '68%' : '83%'}">
    <div class="header">
      <div class="buttons">
        <button
            type="button"
            class="router-link"
            :disabled="props.num_phase === 0"
            @click="() => {
              show_intro = true
              $emit('previousOne', props.num_phase - 1)
            }"
        >Wróć</button>
        <button
            type="button"
            class="router-link"
            :disabled="moveForward()"
            @click="() => {
              show_intro = true
              $emit('nextOne', props.num_phase + 1)
            }"
        >Dalej</button>
      </div>
      <div class="icon fa fa-question-circle" @click.prevent="show_intro = !show_intro"></div>
    </div>

    <ModelDescription v-if="props.num_phase === 0" @confirm="args => current = args"></ModelDescription>

    <ModelLanguage v-if="props.num_phase === 1" @confirm="args => current = args"></ModelLanguage>

    <ModelVersion v-if="props.num_phase === 2" @confirm="args => current = args"></ModelVersion>

    <ModelOverview v-if="props.num_phase === 3" @confirm="args => current = args"></ModelOverview>

    <PrepareData v-if="props.num_phase === 4"></PrepareData>

  </div>
</template>

<style scoped>
.header {
  height: 20%;
  display: flex;
  flex-direction: row;
  justify-content: end;
  align-items: center;
  background-color: #bbb;
}

.router-link {
  height: 200%;
}

.buttons {
  width: 90%;
  height: 30%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}

.icon {
  width: 10%;
  font-size: 300%;
  text-align: center;
}

.model {
  height: 70%;
  width: 100%;
  display: flex;
  flex-direction: column;
}
</style>