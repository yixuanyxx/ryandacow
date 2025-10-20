<template>
  <Transition name="notification">
    <div v-if="isVisible" class="fixed top-4 right-4 z-50 max-w-sm">
      <div :class="notificationClasses" class="p-4 rounded-lg shadow-lg border">
        <div class="flex items-start gap-3">
          <div class="flex-shrink-0">
            <svg v-if="type === 'success'" class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <svg v-else-if="type === 'error'" class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-900">{{ title }}</p>
            <p v-if="message" class="text-sm text-gray-600 mt-1">{{ message }}</p>
          </div>
          <button @click="close" class="flex-shrink-0 text-gray-400 hover:text-gray-600">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script>
import { computed, defineComponent } from 'vue'

export default defineComponent({
  name: 'Notification',
  props: {
    isVisible: {
      type: Boolean,
      default: false
    },
    type: {
      type: String,
      default: 'success',
      validator: (value) => ['success', 'error', 'info'].includes(value)
    },
    title: {
      type: String,
      required: true
    },
    message: {
      type: String,
      default: ''
    }
  },
  emits: ['close'],
  setup(props, { emit }) {
    const notificationClasses = computed(() => {
      const baseClasses = 'bg-white border rounded-lg'
      
      switch (props.type) {
        case 'success':
          return `${baseClasses} border-green-200`
        case 'error':
          return `${baseClasses} border-red-200`
        default:
          return `${baseClasses} border-gray-200`
      }
    })
    
    const close = () => {
      emit('close')
    }
    
    return {
      notificationClasses,
      close
    }
  }
})
</script>

<style scoped>
.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>
