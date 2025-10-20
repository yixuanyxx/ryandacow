<template>
  <div class="notification-container">
    <Notification
      v-for="notification in notifications"
      :key="notification.id"
      :is-visible="notification.isVisible"
      :type="notification.type"
      :title="notification.title"
      :message="notification.message"
      @close="removeNotification(notification.id)"
    />
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import Notification from './Notification.vue'
import { useNotifications } from '@/composables/useNotifications.js'

export default defineComponent({
  name: 'NotificationContainer',
  components: { Notification },
  setup() {
    const { notifications, removeNotification } = useNotifications()
    
    return {
      notifications,
      removeNotification
    }
  }
})
</script>
