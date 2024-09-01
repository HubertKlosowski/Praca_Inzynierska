<script setup>

</script>

<template>
  <div class="container">
    <div class="contact">
      <p>Kontakt</p>
      <p>Telefon: 123-321-231</p>
      <p>Email: a@a.com</p>
    </div>
    <div class="more_info">
      Więcej infomacji na temat depresji można znaleźć <a href="https://www.who.int/news-room/fact-sheets/detail/depression" target="_blank">tutaj</a>
    </div>
    <div class="social_media">
      <a href="https://www.facebook.com/" target="_blank"><img src="@/assets/facebook.png" alt="Facebook icon"></a>
      <a href="https://www.reddit.com/?rdt=51348" target="_blank"><img src="@/assets/reddit.png" alt="Reddit icon"></a>
      <a href="https://x.com/" target="_blank"><img src="@/assets/twitter.png" alt="Twitter icon"></a>
    </div>
    <div class="thanks">
      <h3>Specjalne podziękowania dla https://www.flaticon.com/ za udostępnienie ikon dla mojej strony.</h3>
    </div>
  </div>
</template>

<style scoped>
.container {
  flex: 0.5;
  background-color: cornflowerblue;
  color: white;
  text-align: center;
  padding: 10px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  border-top: 2px black solid;
}

.social_media {
  display: flex;
  flex-direction: row;
  gap: 20px;
}

img {
  width: 10%;
  height: auto;
}
</style>