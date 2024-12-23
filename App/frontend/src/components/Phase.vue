<script setup>
import {ref} from "vue";
import PhaseIntro from "@/components/PhaseIntro.vue";
import PrepareData from "@/components/PrepareData.vue";
import LoadingScreen from "@/components/LoadingScreen.vue";
import _ from "lodash";
import {useRouter} from "vue-router";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";


const router = useRouter()

const props = defineProps(['phase'])
const global_num_phase = defineModel('global_num_phase')
const show_loading_screen = ref(false)
const user = ref(JSON.parse(localStorage.getItem('user')))

const show_intro = ref(true)

const goHome = async () => {
  await router.push('/')
}
</script>

<template>

  <LoadingScreen v-if="show_loading_screen"></LoadingScreen>

  <PhaseIntro v-if="show_intro" v-model="show_intro" :phase="props.phase"></PhaseIntro>

  <div class="model" v-else>
    <div class="main-header">
      <font-awesome-icon :icon="['fas', 'house']" class="router-link" @click="goHome" style="width: 10%;" />
      <RouterLink to="/create_file" class="router-link" v-if="!_.isEmpty(user)" style="width: 20%;">Kreator plików</RouterLink>
      <font-awesome-icon :icon="['fas', 'circle-info']" class="router-link" @click="show_intro = !show_intro" style="width: 10%;" />
    </div>

    <PrepareData v-if="global_num_phase === 0" v-model:show_loading_screen="show_loading_screen"></PrepareData>

  </div>
</template>

<style scoped>
.router-link {
  height: 40%;
  padding: 0.5rem;
}

.main-header {
  width: 100%;
  height: 20%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}

.model {
  height: 85%;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>