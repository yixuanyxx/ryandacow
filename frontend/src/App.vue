<template>
  <div id="app">
    <router-view />
    <NotificationContainer />
  </div>
</template>

<script>
import NotificationContainer from '@/components/common/NotificationContainer.vue'

export default {
  name: 'App',
  components: { NotificationContainer }
}
</script>
