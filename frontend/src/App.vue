<template>
  <main>
    <AppHeader />
    <router-view />
  </main>
</template>

<script>
import AppHeader from './components/header.vue';

  export default {
    components: { AppHeader }
  }

</script>