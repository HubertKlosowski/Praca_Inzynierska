<script setup>

</script>

<template>
  <div class="footer">
    <div class="contact">
      <h3>Kontakt</h3>
      <p>Phone: 123-321-231</p>
      <p>Email: <a href="mailto:a@a.com">hklosowski@interia.com</a></p>
    </div>
    <div class="social_media">
      <a href="https://www.facebook.com/" target="_blank">
        <img src="@/assets/facebook.png" alt="Facebook">
      </a>
      <a href="https://www.reddit.com/" target="_blank">
        <img src="@/assets/reddit.png" alt="Reddit">
      </a>
      <a href="https://x.com/" target="_blank">
        <img src="@/assets/twitter.png" alt="Twitter">
      </a>
    </div>
    <div class="thanks">
      <p>
        Podziękowania dla strony <a href="https://www.flaticon.com/" target="_blank">Flaticon</a>
        za udostępnienie ikon.
      </p>
    </div>
  </div>
</template>

<style scoped>
.footer {
  background-color: #1e3a8a;
  color: white;
  padding: 20px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  border-top: 3px solid black;
  font-family: Arial, sans-serif;
  text-align: center;
}

.footer > * {
  position: relative;
  animation-name: toTheTop;
  animation-duration: 4s;
  animation-timing-function: linear;
}

.contact {
  flex: 1;
  padding: 10px;
}

.contact a {
  color: #f0f0f0;
  text-decoration: none;
}

.contact a:hover {
  text-decoration: underline;
}

.social_media {
  flex: 1;
  display: flex;
  justify-content: center;
  gap: 20px;
}

.social_media img {
  width: 40px;
  height: auto;
  transition: transform 0.3s ease;
}

.social_media img:hover {
  transform: scale(1.1);
}

.thanks {
  flex: 1;
  font-size: 1.2rem;
  padding: 10px;
}

.thanks a {
  color: #ffd700;
  text-decoration: none;
}

.thanks a:hover {
  text-decoration: underline;
}
</style>
