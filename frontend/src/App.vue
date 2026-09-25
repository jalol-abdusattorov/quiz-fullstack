<template>
  <main>
    <AppHeader v-if="isComponentVisible"/>
    <router-view />
  </main>
</template>

<script>
import { useRoute } from 'vue-router';
import AppHeader from './components/AppHeader.vue';
import { computed } from 'vue';

  export default {
    components: { AppHeader },
    setup() {
      const route = useRoute()
      const isComponentVisible = computed(() => {
        return route.meta.showGlobalComponent !== false
      })

      return { isComponentVisible }
    }
  }

</script>