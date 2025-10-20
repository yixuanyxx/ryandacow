import { ref } from 'vue'

const notifications = ref([])

export function useNotifications() {
  const showNotification = (title, message = '', type = 'success', duration = 3000) => {
    const id = Date.now()
    const notification = {
      id,
      title,
      message,
      type,
      isVisible: true
    }
    
    notifications.value.push(notification)
    
    // Auto-remove after duration
    setTimeout(() => {
      removeNotification(id)
    }, duration)
    
    return id
  }
  
  const removeNotification = (id) => {
    const index = notifications.value.findIndex(n => n.id === id)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
  }
  
  const showSuccess = (title, message = '') => {
    return showNotification(title, message, 'success')
  }
  
  const showError = (title, message = '') => {
    return showNotification(title, message, 'error')
  }
  
  return {
    notifications,
    showNotification,
    removeNotification,
    showSuccess,
    showError
  }
}
