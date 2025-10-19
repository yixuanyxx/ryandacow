<template>
  <div class="mx-auto max-w-[1200px] px-4 lg:px-6 py-6 min-h-screen">
    <!-- Header -->
    <header class="mb-6">
      <div class="flex items-center justify-between">
        <h1 class="text-xl font-semibold">PSA Workforce AI</h1>
        <div class="flex gap-3">
          <BaseButton variant="secondary" @click="goToChat">💬 Chat</BaseButton>
          <BaseButton variant="secondary" @click="handleLogout">Logout</BaseButton>
        </div>
      </div>
    </header>

    <!-- Welcome / Profile -->
    <section class="card glass p-5 mb-6">
      <div class="flex items-start justify-between gap-4">
        <div>
          <h2 class="text-lg font-semibold">Welcome, {{ user?.name }}</h2>
          <p class="text-[var(--muted)] mt-1">
            {{ user?.job_title }} • {{ user?.department }}
          </p>
          <div class="mt-3 rounded-lg bg-[var(--panel,#f1f5f9)] border border-white/10 px-3 py-2">
            <span class="font-semibold">🎯 Career Goal:</span>
            <span class="ml-1">Senior {{ user?.job_title }} (2–3 years)</span>
          </div>
        </div>
        <div class="hidden sm:block text-right text-sm text-[var(--muted)]">
          <div>Signed in</div>
        </div>
      </div>
    </section>

    <!-- AI Recommendations -->
    <section class="card glass p-5">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-base font-semibold">💡 AI Recommendations</h3>
        <BaseButton variant="secondary" size="small" @click="goToChat">Ask AI</BaseButton>
      </div>

      <div v-if="isLoading" class="py-10 text-center text-[var(--muted)]">
        Loading recommendations…
      </div>

      <div v-else-if="recommendations.length === 0" class="py-10 text-center text-[var(--muted)]">
        No recommendations available right now.
      </div>

      <div v-else class="grid gap-4 md:grid-cols-2">
        <!-- Course -->
        <div v-if="courseRecommendation" class="card p-4">
          <div class="font-medium mb-1">📚 {{ courseRecommendation.title }}</div>
          <div class="text-sm text-[var(--muted)] mb-2">
            {{ courseRecommendation.description }}
          </div>
          <div class="text-xs text-[var(--muted)] mb-3">
            Match: {{ courseRecommendation.match_score }}% • Duration: {{ courseRecommendation.metadata?.duration_weeks }} weeks
          </div>
          <BaseButton variant="secondary" size="small">View Details</BaseButton>
        </div>

        <!-- Mentor -->
        <div v-if="mentorRecommendation" class="card p-4">
          <div class="font-medium mb-1">🤝 {{ mentorRecommendation.title }}</div>
          <div class="text-sm text-[var(--muted)] mb-2">
            {{ mentorRecommendation.description }}
          </div>
          <div class="text-xs text-[var(--muted)] mb-3">
            Match: {{ mentorRecommendation.match_score }}% • {{ mentorRecommendation.metadata?.experience_years }} yrs experience
          </div>
          <BaseButton variant="secondary" size="small">Connect</BaseButton>
        </div>

        <!-- Career Path -->
        <div v-if="careerRecommendation" class="card p-4 md:col-span-2">
          <div class="font-medium mb-1">🎯 {{ careerRecommendation.title }}</div>
          <div class="text-sm text-[var(--muted)] mb-2">
            {{ careerRecommendation.description }}
          </div>
          <div class="text-xs text-[var(--muted)] mb-3">
            Skills needed: {{ (careerRecommendation.metadata?.required_skills || []).join(', ') }}
          </div>
          <BaseButton variant="secondary" size="small">View Path</BaseButton>
        </div>
      </div>

      <div class="text-center mt-6">
        <BaseButton @click="goToChat">💬 Chat with AI for personalized advice</BaseButton>
      </div>
    </section>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth.js'
import BaseButton from '@/components/common/BaseButton.vue'
import api from '@/services/apiRecs.js'

export default {
  name: 'DashboardPage',
  components: { BaseButton },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()

    const recommendations = ref([])
    const isLoading = ref(false)
    const user = computed(() => authStore.user)

    const courseRecommendation = computed(() =>
      recommendations.value.find((rec) => rec.type === 'course')
    )
    const mentorRecommendation = computed(() =>
      recommendations.value.find((rec) => rec.type === 'mentor')
    )
    const careerRecommendation = computed(() =>
      recommendations.value.find((rec) => rec.type === 'career')
    )

    const fetchRecommendations = async () => {
      if (!user.value?.id) return
      isLoading.value = true
      try {
        const { data } = await apiRecs.get(`/recommendations/${user.value.id}`)
        if (data?.Message === 'Success') {
          recommendations.value = data.data?.recommendations || []
        }
      } catch {
        // keep UI calm
      } finally {
        isLoading.value = false
      }
    }

    const goToChat = () => router.push('/chat')
    const handleLogout = () => { authStore.logout(); router.push('/login') }

    onMounted(fetchRecommendations)

    return {
      user,
      recommendations,
      isLoading,
      courseRecommendation,
      mentorRecommendation,
      careerRecommendation,
      goToChat,
      handleLogout
    }
  }
}
</script>

<style scoped>
/* cards inherit the global “glass” look; spacing handled with utilities */
</style>