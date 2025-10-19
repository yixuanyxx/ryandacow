<!-- views/ChatbotPage.vue -->
<template>
  <div class="chat-container">
    <!-- Header -->
    <div class="header">
      <div class="flex items-center gap-4">
        <BaseButton variant="secondary" @click="goBack">
          ← Back
        </BaseButton>
        <h1>Chat with Career AI</h1>
      </div>
      <BaseButton variant="secondary" @click="clearChat">
        Clear
      </BaseButton>
    </div>

    <!-- Messages -->
    <div class="chat-messages" ref="messagesContainer">
      <div
        v-for="message in chatStore.messages"
        :key="message.id"
        :class="['message', message.type === 'ai' ? 'message-ai' : 'message-user']"
      >
        <div style="font-weight: 600; margin-bottom: 4px;">
          {{ message.type === 'ai' ? '🤖 AI' : '👤 You' }}
        </div>
        <div>{{ message.content }}</div>
      </div>
      
      <div v-if="chatStore.isLoading" class="message message-ai">
        <div style="font-weight: 600; margin-bottom: 4px;">🤖 AI</div>
        <div>Thinking...</div>
      </div>
    </div>

    <!-- Input -->
    <div class="chat-input-container">
      <input
        v-model="newMessage"
        type="text"
        placeholder="Type your message..."
        class="chat-input"
        @keypress.enter="sendMessage"
        :disabled="chatStore.isLoading"
      />
      <BaseButton 
        @click="sendMessage"
        :disabled="!newMessage.trim() || chatStore.isLoading"
      >
        Send →
      </BaseButton>
    </div>
  </div>
</template>

<script>
import { ref, nextTick, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth.js'
import { useChatStore } from '@/store/chat.js'
import { chatService } from '@/services/chatService.js'
import BaseButton from '@/components/common/BaseButton.vue'

export default {
  name: 'ChatbotPage',
  components: {
    BaseButton
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const chatStore = useChatStore()
    
    const newMessage = ref('')
    const messagesContainer = ref(null)

    const scrollToBottom = () => {
      nextTick(() => {
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
        }
      })
    }

    const sendMessage = async () => {
      if (!newMessage.value.trim() || chatStore.isLoading) return

      const message = newMessage.value.trim()
      newMessage.value = ''

      // Add user message
      chatStore.addMessage({
        type: 'user',
        content: message
      })

      scrollToBottom()

      // Send to AI
      chatStore.setLoading(true)
      try {
        const result = await chatService.sendMessage(message, authStore.user?.id)
        
        if (result.success) {
          chatStore.addMessage({
            type: 'ai',
            content: result.response
          })
        } else {
          chatStore.addMessage({
            type: 'ai',
            content: 'Sorry, I encountered an error. Please try again.'
          })
        }
      } catch (error) {
        chatStore.addMessage({
          type: 'ai',
          content: 'Sorry, I encountered an error. Please try again.'
        })
      } finally {
        chatStore.setLoading(false)
        scrollToBottom()
      }
    }

    const goBack = () => {
      router.push('/dashboard')
    }

    const clearChat = () => {
      chatStore.clearMessages()
    }

    onMounted(() => {
      scrollToBottom()
    })

    return {
      chatStore,
      newMessage,
      messagesContainer,
      sendMessage,
      goBack,
      clearChat
    }
  }
}
</script>
