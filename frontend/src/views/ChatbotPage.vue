<!-- src/views/ChatbotPage.vue -->
<script>
import { ref, nextTick, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth.js'
import { useChatStore } from '@/store/chat.js'
import { chatService } from '@/services/chatService.js'

import BaseButton from '@/components/common/BaseButton.vue'
import CareerPlanCard from '@/components/ai/CareerPlanCard.vue'
import LeadershipBadge from '@/components/ai/LeadershipBadge.vue'
import MarkdownText from '@/components/common/MarkdownText.vue'
import RightPanelEmpty from '@/components/ai/RightPanelEmpty.vue'
import SkeletonBox from '@/components/common/SkeletonBox.vue'

export default {
  name: 'ChatbotPage',
  components: { BaseButton, CareerPlanCard, LeadershipBadge, MarkdownText, RightPanelEmpty, SkeletonBox },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const chatStore = useChatStore()

    const newMessage = ref('')
    const messagesContainer = ref(null)

    const scrollToBottom = () => {
      nextTick(() => {
        const el = messagesContainer.value
        if (el) el.scrollTop = el.scrollHeight
      })
    }

    const hydrateRightPanel = (payload = {}) => {
      const { plan, leadership, feedback } = payload
      if (plan) chatStore.setLastPlan?.(plan)
      if (leadership) chatStore.setLastLeadership?.(leadership)
      if (feedback) chatStore.setLastFeedback?.(feedback)
    }

    const sendMessage = async () => {
      if (!newMessage.value.trim() || chatStore.isLoading) return
      const message = newMessage.value.trim()
      newMessage.value = ''

      // user bubble
      chatStore.addMessage({ type: 'user', content: message })
      scrollToBottom()

      chatStore.setLoading(true)
      try {
        const result = await chatService.sendMessage(message, authStore.user?.id || 1)

        if (result?.success) {
          // ai bubble
          const text = result.responseText || '(no summary)'
          chatStore.addMessage({ type: 'ai', content: text })
          hydrateRightPanel(result.payload)
        } else {
          chatStore.addMessage({ type: 'ai', content: result?.error || 'Sorry, I encountered an error. Please try again.' })
        }
      } catch (e) {
        chatStore.addMessage({ type: 'ai', content: 'Sorry, I encountered an error. Please try again.' })
      } finally {
        chatStore.setLoading(false)
        scrollToBottom()
      }
    }

    // when a suggestion chip is clicked in the right panel
    const pickSuggestion = (q) => {
      if (!q) return
      newMessage.value = q
      // optional: show it in the input first; remove next line to send immediately
      // return
      sendMessage()
    }

    const goBack = () => router.push('/dashboard')
    const clearChat = () => chatStore.clearMessages()

    onMounted(scrollToBottom)

    return {
      chatStore,
      newMessage,
      messagesContainer,
      sendMessage,
      pickSuggestion,
      goBack,
      clearChat
    }
  }
}
</script>

<template>
  <div class="page-grid">
    <!-- LEFT: chat -->
    <section class="chat-container">
      <div class="header">
        <div class="flex items-center gap-4">
          <BaseButton variant="secondary" @click="goBack">← Back</BaseButton>
          <h1>Chat with Career AI</h1>
        </div>
        <BaseButton variant="secondary" @click="clearChat">Clear</BaseButton>
      </div>

      <div class="chat-messages" ref="messagesContainer">
        <div
          v-for="message in chatStore.messages"
          :key="message.id"
          :class="['message', message.type === 'ai' ? 'message-ai' : 'message-user']"
        >
          <div style="font-weight:600;margin-bottom:4px;">
            {{ message.type === 'ai' ? '🤖 AI' : '👤 You' }}
          </div>

          <!-- render AI as markdown -->
          <div v-if="message.type==='ai'">
            <MarkdownText :text="message.content" />
          </div>
          <div v-else>
            {{ message.content }}
          </div>
        </div>

        <div v-if="chatStore.isLoading" class="message message-ai">
          <div style="font-weight:600; margin-bottom:4px;">🤖 AI</div>
          <div>Thinking...</div>
        </div>
      </div>

      <div class="chat-input-container">
        <input
          v-model="newMessage"
          type="text"
          placeholder="Type your message..."
          class="chat-input"
          @keydown.enter="sendMessage"
          :disabled="chatStore.isLoading"
        />
        <BaseButton @click="sendMessage" :disabled="!newMessage.trim() || chatStore.isLoading">
          Send →
        </BaseButton>
      </div>
    </section>

    <!-- RIGHT: plan panel -->
    <aside class="panel">
      <template v-if="chatStore.isLoading">
        <SkeletonBox />
      </template>

      <template v-else>
        <template v-if="chatStore.lastLeadership || chatStore.lastPlan">
          <LeadershipBadge v-if="chatStore.lastLeadership" :leadership="chatStore.lastLeadership" />
          <CareerPlanCard v-if="chatStore.lastPlan" :plan="chatStore.lastPlan" />
          <div v-if="chatStore.lastFeedback" class="card">
            <h3>🧭 Recommended Actions</h3>
            <ul>
              <li v-for="(a,i) in chatStore.lastFeedback.recommended_actions" :key="i">{{ a }}</li>
            </ul>
          </div>
        </template>

        <RightPanelEmpty
          v-else
          @use="pickSuggestion"
        />
      </template>
    </aside>
  </div>
</template>

<style scoped>
.page-grid { display:grid; grid-template-columns: 2fr 1fr; gap:16px; }
.panel .card { margin-top: 12px; }
</style>