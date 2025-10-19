<!-- src/views/ChatbotPage.vue -->
<script>
import { ref, nextTick, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/store/auth.js";
import { useChatStore } from "@/store/chat.js";
import { chatService } from "@/services/chatService.js";

import BaseButton from "@/components/common/BaseButton.vue";
import CareerPlanCard from "@/components/ai/CareerPlanCard.vue";
import LeadershipBadge from "@/components/ai/LeadershipBadge.vue";
import MarkdownText from "@/components/common/MarkdownText.vue";
import RightPanelEmpty from "@/components/ai/RightPanelEmpty.vue";
import SkeletonBox from "@/components/common/SkeletonBox.vue";
import MessageBubble from "@/components/ai/MessageBubble.vue";
import PlanGauge from "@/components/ai/PlanGauge.vue";
import TopGaps from "@/components/ai/TopGaps.vue";
import QuickWins from "@/components/ai/QuickWins.vue";

export default {
  name: "ChatbotPage",
  components: {
    BaseButton,
    CareerPlanCard,
    LeadershipBadge,
    MarkdownText,
    RightPanelEmpty,
    SkeletonBox,
    MessageBubble,
    PlanGauge,
    TopGaps,
    QuickWins,
  },
  setup() {
    const router = useRouter();
    const authStore = useAuthStore();
    const chatStore = useChatStore();

    const newMessage = ref("");
    const messagesContainer = ref(null);

    const scrollToBottom = () => {
      nextTick(() => {
        const el = messagesContainer.value;
        if (el) el.scrollTop = el.scrollHeight;
      });
    };

    const hydrateRightPanel = (payload = {}) => {
      const { plan, leadership, feedback } = payload;
      if (plan) chatStore.setLastPlan?.(plan);
      if (leadership) chatStore.setLastLeadership?.(leadership);
      if (feedback) chatStore.setLastFeedback?.(feedback);
    };

    const sendMessage = async () => {
      if (!newMessage.value.trim() || chatStore.isLoading) return;
      const message = newMessage.value.trim();
      newMessage.value = "";

      // user bubble
      chatStore.addMessage({ type: "user", content: message });
      scrollToBottom();

      chatStore.setLoading(true);
      try {
        const result = await chatService.sendMessage(
          message,
          authStore.user?.id || 1
        );

        if (result?.success) {
          // ai bubble
          const text = result.responseText || "(no summary)";
          chatStore.addMessage({ type: "ai", content: text });
          hydrateRightPanel(result.payload);
        } else {
          chatStore.addMessage({
            type: "ai",
            content:
              result?.error ||
              "Sorry, I encountered an error. Please try again.",
          });
        }
      } catch (e) {
        chatStore.addMessage({
          type: "ai",
          content: "Sorry, I encountered an error. Please try again.",
        });
      } finally {
        chatStore.setLoading(false);
        scrollToBottom();
      }
    };

    // when a suggestion chip is clicked in the right panel
    const pickSuggestion = (q) => {
      if (!q) return;
      newMessage.value = q;
      // optional: show it in the input first; remove next line to send immediately
      // return
      sendMessage();
    };

    const goBack = () => router.push("/dashboard");
    const clearChat = () => chatStore.clearMessages();

    onMounted(scrollToBottom);

    return {
      chatStore,
      newMessage,
      messagesContainer,
      sendMessage,
      pickSuggestion,
      goBack,
      clearChat,
    };
  },
};
</script>

<!-- keep your <script> as-is -->

<template>
  <div class="mx-auto max-w-[1200px] px-4 lg:px-6 py-4 lg:py-6 min-h-screen">
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- LEFT: chat -->
      <section class="lg:col-span-2 card glass p-4 lg:p-6 vh-panel flex flex-col">
        <!-- header -->
        <div class="mb-4 pb-3 border-b border-white/10">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <BaseButton variant="secondary" @click="goBack">← Back</BaseButton>
              <h1 class="text-lg font-semibold">Chat with Career AI</h1>
            </div>
            <BaseButton variant="secondary" @click="clearChat">Clear</BaseButton>
          </div>
        </div>

        <!-- messages -->
        <div ref="messagesContainer" class="flex-1 overflow-y-auto scroll-slim pr-1">
          <transition-group name="fade" tag="div">
            <MessageBubble
              v-for="message in chatStore.messages"
              :key="message.id"
              :mine="message.type !== 'ai'"
            >
              <template v-if="message.type === 'ai'">
                <div class="md"><MarkdownText :text="message.content" /></div>
              </template>
              <template v-else>{{ message.content }}</template>
            </MessageBubble>
          </transition-group>

          <MessageBubble v-if="chatStore.isLoading">Thinking...</MessageBubble>
        </div>

        <!-- input -->
        <div class="mt-4 flex items-center gap-2">
          <input
            v-model="newMessage"
            type="text"
            placeholder="Type your message..."
            class="flex-1 rounded-xl bg-[var(--panel)] border border-white/10 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-brand/50"
            @keydown.enter="sendMessage"
            :disabled="chatStore.isLoading"
          />
          <BaseButton @click="sendMessage" :disabled="!newMessage.trim() || chatStore.isLoading">
            Send →
          </BaseButton>
        </div>
      </section>

      <!-- RIGHT: plan panel -->
      <aside class="card glass p-4 lg:p-6 vh-panel overflow-y-auto scroll-slim lg:sticky lg:top-6">
        <template v-if="chatStore.isLoading">
          <SkeletonBox />
        </template>

        <template v-else>
          <template v-if="chatStore.lastLeadership || chatStore.lastPlan">
            <div class="panel-stack">
              <LeadershipBadge v-if="chatStore.lastLeadership" :leadership="chatStore.lastLeadership" />
              <PlanGauge v-if="chatStore.lastPlan" :value="chatStore.lastPlan.fit_score || 0" />
              <CareerPlanCard v-if="chatStore.lastPlan" :plan="chatStore.lastPlan" />
              <TopGaps v-if="chatStore.lastPlan?.missing_skills?.length" :gaps="chatStore.lastPlan.missing_skills" />
              <QuickWins @send="pickSuggestion" />
              <div v-if="chatStore.lastFeedback" class="card p-3">
                <h3 class="text-sm text-[var(--muted)] mb-2">🧭 Recommended Actions</h3>
                <ul class="list-disc pl-4 space-y-1 text-sm">
                  <li v-for="(a,i) in chatStore.lastFeedback.recommended_actions" :key="i">{{ a }}</li>
                </ul>
              </div>
            </div>
          </template>

          <RightPanelEmpty v-else @use="pickSuggestion" />
        </template>
      </aside>
    </div>
  </div>
</template>

<style scoped>
/* smooth message fades */
.fade-enter-active, .fade-leave-active { transition: opacity .2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* viewport panel height (accounts for page paddings/header) */
.vh-panel { height: calc(100vh - 8rem); }   /* tweak once and it fixes both columns */
@media (min-width: 1024px) {
  .vh-panel { height: calc(100vh - 7rem); }
}

/* uniform vertical rhythm in the right column */
.panel-stack > * + * { margin-top: 16px; }

/* optional: thinner scrollbars */
.scroll-slim::-webkit-scrollbar { width: 8px; }
.scroll-slim::-webkit-scrollbar-thumb { background: rgba(255,255,255,.15); border-radius: 8px; }
.scroll-slim::-webkit-scrollbar-track { background: transparent; }
</style>