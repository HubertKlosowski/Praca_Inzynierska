<script setup>
import _ from "lodash";
import {onMounted, ref} from "vue";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import ResponseOutput from "@/components/ResponseOutput.vue";


const stats = ref(JSON.parse(localStorage.getItem('depressed')))
const text = ref(JSON.parse(localStorage.getItem('text')))
const submission = ref(JSON.parse(localStorage.getItem('choosen_submission')))
const user = ref(JSON.parse(localStorage.getItem('user')))
const time = ref(0)
const records = ref(0)
const after_create = ref([])
const title = ref('Co to są "trudne" rekordy?')
const subtitle = ref('Są to rekordy, którym nie da się jednoznacznie określić występowania depresji. ' +
    'Jej wartość dla takich wpisów znajduję się w przedziale od 45% do 55% włącznie. ')
const response_status = defineModel('response_status')


const hardToAccess = () => {
  let res = _.filter(stats.value, function (num) {
    return num > 0.45 && num < 0.55
  })
  return _.size(res)
}

const counter = (variable, target, duration) => {
  const steps = Math.ceil(duration / 64)
  const step = (target - variable.value) / steps
  const interval = duration / steps

  const update = () => {
    if (variable.value >= target || Math.abs(variable.value - target) < step) {
      variable.value = target
    } else {
      variable.value += step
      variable.value = Math.round(variable.value * 100) / 100
      setTimeout(update, interval)
    }
  }
  update()
}

const non_decisive_rows = ref(hardToAccess())

onMounted(() => {
  const end_time = submission.value['time_taken'].toFixed(2)
  const end_records = text.value.length

  counter(time, end_time, 1000)
  counter(records, end_records, 1000)
})
</script>

<template>

  <ResponseOutput
      v-if="response_status !== 0"
      v-model:response_status="response_status"
      :after_create="after_create"
      :title="title"
      :subtitle="subtitle"
  ></ResponseOutput>

  <div class="general-info" :style="{
    opacity: response_status < 100 ? '1' : '0.3',
    pointerEvents: response_status < 100 ? 'auto' : 'none'
  }">
    <div class="info">
      <span>Czas wykonania (s)</span>
      <span id="count">{{ time }}</span>
    </div>
    <div class="info" v-if="text.length > 1">
      <span>Liczba rekordów</span>
      <span>{{ records }}</span>
    </div>
    <div class="info" v-else style="justify-content: center">
      Pojedynczy wpis
    </div>
    <div class="info" v-if="non_decisive_rows !== 0">
      <span>
        "Trudne" rekordy:
        <font-awesome-icon :icon="['fas', 'circle-info']" class="router-link" @click="response_status = 100"/>
      </span>
      <span>{{ non_decisive_rows }}</span>
    </div>
    <div class="info" v-else style="justify-content: center">
      Brak "trudnych" rekordów
      <font-awesome-icon :icon="['fas', 'circle-info']" class="router-link" @click="response_status = 100"/>
    </div>
    <div class="info">
      <span>Użytkownik</span>
      <span>{{ user['username'] }}</span>
    </div>
    <div class="info">
      <span>Nazwa modelu</span>
      <span>{{ submission['model'] }}</span>
    </div>
  </div>
</template>

<style scoped>
.router-link {
  height: 40%;
}

span {
  text-align: center;
}

.info {
  width: 100%;
  height: 10%;
  border-top-left-radius: 0.75rem;
  border-bottom-left-radius: 0.75rem;
  background: rgb(71, 71, 71);
  background: linear-gradient(90deg, rgba(71, 71, 71, 1) 0%, rgba(245, 245, 245, 1) 100%);
  text-align: center;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
  padding: 1rem;
}

.general-info {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
}
</style>