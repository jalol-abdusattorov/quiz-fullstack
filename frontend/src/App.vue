<template>
  <main>
    <AppHeader />
    <router-view />
  </main>
</template>

<script>
import AppHeader from './components/AppHeader.vue';

  export default {
    components: { AppHeader }
  }

</script>