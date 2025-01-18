<script setup>
import axios from "axios";
import {inject, onMounted, reactive, ref} from "vue";
import ResponseOutput from "@/components/ResponseOutput.vue";


const move_to = ref('')
const user = ref(JSON.parse(localStorage.getItem('user')))
const $cookies = inject('$cookies')

const after_create = ref({})
const title = ref('')
const subtitle = ref('')
const response_status = ref(0)
const token = reactive(JSON.parse(localStorage.getItem('token')))

const deleteUser = async () => {
  try {
    const token = JSON.parse(localStorage.getItem('token'))
    const response = await axios.delete('http://localhost:8000/api/user/delete_user',
        {headers: {'Authorization' : `Bearer ${token['access']}`}}
    )

    after_create.value = [
      ['Nazwa użytkownika', user.value['username']],
      ['Adres email', user.value['email']],
    ]
    title.value = response.data.success
    subtitle.value = 'Użytkownik został poprawnie usunięty.'
    response_status.value = response.status

    localStorage.clear()
    localStorage.setItem('choosen_model', JSON.stringify('bert-base'))
    $cookies.remove('made_submission')
    move_to.value = '/'

  } catch (e) {
    if (typeof e.response === 'undefined') {
      after_create.value = ['Nie udało się połączyć z serwerem.']
      response_status.value = 500
      title.value = 'Problem z serwerem'
      subtitle.value = 'Proszę poczekać, serwer nie jest teraz dostępny.'
    } else {
      const error_response = e.response
      response_status.value = error_response.status
      after_create.value = error_response.data.error
      subtitle.value = 'Próba usunięcia konta użytkownika się nie powiodła. Proszę zapoznać się z komunikatami wyświetlanymi poniżej:'

      if (response_status.value === 429) {
        title.value = 'Przekroczony limit zmian danych użytkownika'
      } else if (response_status.value === 403) {
        title.value = 'Problem z weryfikacją użytkownika'
        if (error_response.data.code === 'access_token_failed') {  // jeśli access_token wygaśnie
          await refreshAccessToken(['Twoje dane wygasły, ale zostały odświeżone.', 'Teraz możesz usunąć konto użytkownika.'])
        }
      } else {
        title.value = 'Problem z danymi'
      }
    }
    move_to.value = '/profile'
  }
}

const refreshAccessToken = async (after_create_success) => {
  try {
    const response = await axios.post('http://localhost:8000/api/token/refresh', {
      'refresh': token.refresh
    })

    token.access = response.data['access']
    localStorage.setItem('token', JSON.stringify(token))

    after_create.value = after_create_success
    response_status.value = 199  // błąd nie spowodowany działaniem użytkownika

  } catch (e) {
    const error_response = e.response
    response_status.value = error_response.status
    after_create.value = error_response.data.error
    title.value = 'Problem z danymi logowania'  // jeśli refresh_token wygaśnie
  }
}

onMounted(async () => {
  await deleteUser()
})
</script>

<template>
  <ResponseOutput
      v-model:response_status="response_status"
      :after_create="after_create"
      v-if="response_status >= 100 && response_status !== 403"
      :move_to="move_to"
      :title="title"
      :subtitle="subtitle"
  ></ResponseOutput>
</template>

<style scoped>

</style>