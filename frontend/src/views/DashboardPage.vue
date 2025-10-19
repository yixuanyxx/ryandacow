<!-- views/DashboardPage.vue -->
<template>
  <div>
    <!-- Header -->
    <div class="header">
      <h1>PSA Workforce AI</h1>
      <div class="flex gap-4 items-center">
        <BaseButton variant="secondary" @click="goToChat">
          💬 Chat
        </BaseButton>
        <BaseButton variant="secondary" @click="handleLogout">
          Logout
        </BaseButton>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container">
      <!-- Welcome Section -->
      <div class="card mb-6">
        <h2 style="font-size: 24px; margin-bottom: 8px;">
          Welcome, {{ user?.name }}
        </h2>
        <p style="color: #64748b; font-size: 16px;">
          {{ user?.job_title }} • {{ user?.department }}
        </p>
        <div style="margin-top: 16px; padding: 12px; background: #f1f5f9; border-radius: 6px;">
          <span style="font-weight: 600;">🎯 Career Goal:</span>
          <span style="margin-left: 8px;">Senior {{ user?.job_title }} (2-3 years)</span>
        </div>
      </div>

      <!-- AI Recommendations -->
      <div class="card">
        <h3 style="font-size: 20px; margin-bottom: 20px; color: #0A2463;">
          💡 AI Recommendations
        </h3>

        <div v-if="isLoading" class="text-center" style="padding: 40px;">
          Loading recommendations...
        </div>

        <div v-else-if="recommendations.length === 0" class="text-center" style="padding: 40px; color: #64748b;">
          No recommendations available at the moment.
        </div>

        <div v-else>
          <!-- Course Recommendation -->
          <div v-if="courseRecommendation" class="recommendation-card">
            <div class="recommendation-title">
              📚 {{ courseRecommendation.title }}
            </div>
            <div class="recommendation-description">
              {{ courseRecommendation.description }}
            </div>
            <div class="recommendation-meta">
              Match: {{ courseRecommendation.match_score }}% • Duration: {{ courseRecommendation.metadata?.duration_weeks }} weeks
            </div>
            <BaseButton variant="secondary" size="small">
              View Details
            </BaseButton>
          </div>

          <!-- Mentor Recommendation -->
          <div v-if="mentorRecommendation" class="recommendation-card">
            <div class="recommendation-title">
              🤝 {{ mentorRecommendation.title }}
            </div>
            <div class="recommendation-description">
              {{ mentorRecommendation.description }}
            </div>
            <div class="recommendation-meta">
              Match: {{ mentorRecommendation.match_score }}% • {{ mentorRecommendation.metadata?.experience_years }} years experience
            </div>
            <BaseButton variant="secondary" size="small">
              Connect
            </BaseButton>
          </div>

          <!-- Career Recommendation -->
          <div v-if="careerRecommendation" class="recommendation-card">
            <div class="recommendation-title">
              🎯 {{ careerRecommendation.title }}
            </div>
            <div class="recommendation-description">
              {{ careerRecommendation.description }}
            </div>
            <div class="recommendation-meta">
              Skills needed: {{ careerRecommendation.metadata?.required_skills?.join(', ') }}
            </div>
            <BaseButton variant="secondary" size="small">
              View Path
            </BaseButton>
          </div>
        </div>

        <!-- Chat Button -->
        <div class="text-center mt-6">
          <BaseButton @click="goToChat" style="padding: 12px 24px; font-size: 16px;">
            💬 Chat with AI for personalized advice
          </BaseButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth.js'
import BaseButton from '@/components/common/BaseButton.vue'
import api from '@/services/api.js'

export default {
  name: 'DashboardPage',
  components: {
    BaseButton
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const recommendations = ref([])
    const isLoading = ref(false)

    const user = computed(() => authStore.user)

    const courseRecommendation = computed(() => 
      recommendations.value.find(rec => rec.type === 'course')
    )

    const mentorRecommendation = computed(() => 
      recommendations.value.find(rec => rec.type === 'mentor')
    )

    const careerRecommendation = computed(() => 
      recommendations.value.find(rec => rec.type === 'career')
    )

    const fetchRecommendations = async () => {
      if (!user.value?.id) return

      isLoading.value = true
      try {
        const response = await api.get(`/api/recommendations/${user.value.id}`)
        if (response.data.Message === 'Success') {
          recommendations.value = response.data.data.recommendations || []
        }
      } catch (error) {
        console.error('Failed to fetch recommendations:', error)
      } finally {
        isLoading.value = false
      }
    }

    const goToChat = () => {
      router.push('/chat')
    }

    const handleLogout = () => {
      authStore.logout()
      router.push('/login')
    }

    onMounted(() => {
      fetchRecommendations()
    })

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
