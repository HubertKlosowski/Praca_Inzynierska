<script setup>
import {ref} from "vue";
import PhaseIntro from "@/components/PhaseIntro.vue";
import ModelDescription from "@/components/ModelDescription.vue";
import ModelLanguage from "@/components/ModelLanguage.vue";
import ModelVersion from "@/components/ModelVersion.vue";
import ModelOverview from "@/components/ModelOverview.vue";
import PrepareData from "@/components/PrepareData.vue";
import LoadingScreen from "@/components/LoadingScreen.vue";

const props = defineProps(['phase'])
const global_num_phase = defineModel('global_num_phase')
const show_loading_screen = ref(false)

const show_intro = ref(true)
const current = ref(0)

const moveForward = () => {
  return global_num_phase.value === 5 || current.value < global_num_phase.value
}
</script>

<template>

  <LoadingScreen v-if="show_loading_screen"></LoadingScreen>

  <PhaseIntro v-if="show_intro" v-model="show_intro" :phase="props.phase"></PhaseIntro>

  <div class="model" v-else :style="{ height: global_num_phase === 4 ? '68%' : '83%' }">
    <div class="main-header">
      <div class="buttons">
        <button
            type="button"
            class="router-link"
            :disabled="global_num_phase === 0"
            @click="() => {
              show_intro = true
              global_num_phase -= 1
            }"
        >Wróć</button>
        <button
            type="button"
            class="router-link"
            :disabled="moveForward()"
            @click="() => {
              show_intro = true
              global_num_phase += 1
            }"
        >Dalej</button>
      </div>
      <div class="icon fa fa-question-circle" @click.prevent="show_intro = !show_intro"></div>
    </div>

    <ModelDescription v-if="global_num_phase === 0"></ModelDescription>

    <ModelLanguage v-if="global_num_phase === 1" v-model:current="current"></ModelLanguage>

    <ModelVersion v-if="global_num_phase === 2" v-model:current="current"></ModelVersion>

    <ModelOverview v-if="global_num_phase === 3" v-model:current="current"></ModelOverview>

    <PrepareData v-if="global_num_phase === 4" v-model:show_loading_screen="show_loading_screen"></PrepareData>

  </div>
</template>

<style scoped>
.main-header {
  width: 100%;
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
  font-size: 4vw;
  margin-right: 1rem;
  text-align: center;
}

.model {
  height: 85%;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

@media (max-width: 768px) {
  .icon {
    font-size: 4vh;
  }
}
</style>