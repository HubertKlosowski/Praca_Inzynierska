<script setup>
import {ref} from "vue";
import PhaseIntro from "@/components/PhaseIntro.vue";
import PrepareData from "@/components/PrepareData.vue";
import LoadingScreen from "@/components/LoadingScreen.vue";
import _ from "lodash";


const props = defineProps(['phase'])
const global_num_phase = defineModel('global_num_phase')
const show_loading_screen = ref(false)
const user = ref(JSON.parse(localStorage.getItem('user')))
const to_file = ref(JSON.parse(localStorage.getItem('to_file')))

const show_intro = ref(true)
</script>

<template>

  <LoadingScreen v-if="show_loading_screen"></LoadingScreen>

  <PhaseIntro v-if="show_intro" v-model="show_intro" :phase="props.phase"></PhaseIntro>

  <div class="model" v-else>
    <div class="main-header">
      <RouterLink to="/" class="router-link">Wróć do strony głównej</RouterLink>
      <RouterLink to="/create_file" class="router-link" v-if="!_.isEmpty(user)">Kreator plików</RouterLink>
      <div class="icon fa fa-question-circle" @click.prevent="show_intro = !show_intro"></div>
    </div>

    <PrepareData v-if="global_num_phase === 0" v-model:show_loading_screen="show_loading_screen"></PrepareData>

  </div>
</template>

<style scoped>
.router-link {
  width: 20%;
  height: 100%;
}

.main-header {
  width: 100%;
  height: 10%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
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