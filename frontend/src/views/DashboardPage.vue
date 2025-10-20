<template>
  <div class="min-h-screen bg-slate-900">
    <div class="mx-auto max-w-[1200px] px-4 lg:px-6 py-6">
    <!-- Header -->
    <header class="mb-6">
      <div class="flex items-center justify-between">
        <h1 class="text-xl font-semibold text-white">PSA Workforce AI</h1>
        <div class="flex gap-3">
          <BaseButton variant="secondary" @click="goToProfile">Profile</BaseButton>
          <BaseButton variant="secondary" @click="goToChat">Chat</BaseButton>
          <BaseButton variant="secondary" @click="handleLogout">Logout</BaseButton>
        </div>
      </div>
    </header>

    <!-- Welcome / Profile -->
    <section class="card glass p-5 mb-6">
      <div class="flex items-start justify-between gap-4">
        <div>
          <h2 class="text-lg font-semibold text-white">Welcome, {{ user?.name }}</h2>
          <p class="text-gray-300 mt-1">
            {{ user?.job_title }} - {{ user?.department }}
          </p>
          <div class="mt-3 rounded-lg bg-slate-800 border border-slate-700 px-3 py-2">
            <span class="font-semibold text-white">Career Goal:</span>
            <span class="ml-1 text-gray-300">Senior {{ user?.job_title }} (2-3 years)</span>
          </div>
        </div>
        <div class="hidden sm:block text-right text-sm text-gray-400">
          <div>Signed in</div>
        </div>
      </div>
    </section>

    <!-- AI Recommendations -->
    <section class="card glass p-5">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-base font-semibold text-white">AI Recommendations</h3>
        <BaseButton variant="secondary" size="small" @click="goToChat">Ask AI</BaseButton>
      </div>

      <div v-if="isLoading" class="py-10 text-center text-gray-400">
        Loading recommendations...
      </div>

      <div v-else-if="recommendations.length === 0" class="py-10 text-center text-gray-400">
        No recommendations available right now.
      </div>

      <div v-else class="space-y-4">
        <!-- Course Recommendation -->
        <div v-if="courseRecommendation" class="bg-[var(--recommendation-bg)] border border-[var(--recommendation-border)] p-4 rounded-lg border-l-4 border-l-blue-500">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center gap-2 mb-2">
                <div class="w-6 h-6 bg-blue-500/20 rounded flex items-center justify-center">
                  <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                  </svg>
                </div>
                <span class="text-xs font-medium text-blue-400 uppercase tracking-wide">Course Recommendation</span>
              </div>
              <div class="font-semibold mb-1 text-[var(--recommendation-title)]">{{ courseRecommendation.title }}</div>
              <div class="text-sm text-[var(--recommendation-text)] mb-2">
                {{ courseRecommendation.description }}
              </div>
              <div class="text-xs text-[var(--recommendation-text)] mb-3">
                Match: {{ courseRecommendation.match_score }}% - Duration: {{ courseRecommendation.metadata?.duration_weeks }} weeks
              </div>
            </div>
            <BaseButton variant="secondary" size="small" @click="openCourseModal">View Details</BaseButton>
          </div>
        </div>

        <!-- Mentor Recommendation -->
        <div v-if="mentorRecommendation" class="bg-[var(--recommendation-bg)] border border-[var(--recommendation-border)] p-4 rounded-lg border-l-4 border-l-purple-500">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center gap-2 mb-2">
                <div class="w-6 h-6 bg-purple-500/20 rounded flex items-center justify-center">
                  <svg class="w-4 h-4 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                  </svg>
                </div>
                <span class="text-xs font-medium text-purple-400 uppercase tracking-wide">Mentor Match</span>
              </div>
              <div class="font-semibold mb-1 text-[var(--recommendation-title)]">{{ mentorRecommendation.title }}</div>
              <div class="text-sm text-[var(--recommendation-text)] mb-2">
                {{ mentorRecommendation.description }}
              </div>
              <div class="text-xs text-[var(--recommendation-text)] mb-3">
                Match: {{ mentorRecommendation.match_score }}% - {{ mentorRecommendation.metadata?.experience_years }} yrs experience
              </div>
            </div>
            <BaseButton variant="secondary" size="small" @click="openMentorModal">Connect</BaseButton>
          </div>
        </div>

        <!-- Career Path Recommendation -->
        <div v-if="careerRecommendation" class="bg-[var(--recommendation-bg)] border border-[var(--recommendation-border)] p-4 rounded-lg border-l-4 border-l-green-500">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center gap-2 mb-2">
                <div class="w-6 h-6 bg-green-500/20 rounded flex items-center justify-center">
                  <svg class="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                  </svg>
                </div>
                <span class="text-xs font-medium text-green-400 uppercase tracking-wide">Career Path</span>
              </div>
              <div class="font-semibold mb-1 text-[var(--recommendation-title)]">{{ careerRecommendation.title }}</div>
              <div class="text-sm text-[var(--recommendation-text)] mb-2">
                {{ careerRecommendation.description }}
              </div>
              <div class="text-xs text-[var(--recommendation-text)] mb-3">
                Skills needed: {{ (careerRecommendation.metadata?.required_skills || []).join(', ') }}
              </div>
            </div>
            <BaseButton variant="secondary" size="small" @click="openCareerModal">View Path</BaseButton>
          </div>
        </div>
      </div>

      <div class="text-center mt-6">
        <BaseButton @click="goToChat">Chat with AI for personalized advice</BaseButton>
      </div>
    </section>

    <!-- Modals -->
    <CourseDetailsModal 
      :is-open="isCourseModalOpen" 
      :course="courseRecommendation" 
      @close="closeCourseModal" 
    />
    <MentorConnectModal 
      :is-open="isMentorModalOpen" 
      :mentor="mentorRecommendation" 
      @close="closeMentorModal" 
    />
    <CareerPathModal 
      :is-open="isCareerModalOpen" 
      :career="careerRecommendation" 
      @close="closeCareerModal" 
    />
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth.js'
import BaseButton from '@/components/common/BaseButton.vue'
import CourseDetailsModal from '@/components/modals/CourseDetailsModal.vue'
import MentorConnectModal from '@/components/modals/MentorConnectModal.vue'
import CareerPathModal from '@/components/modals/CareerPathModal.vue'
import api from '@/services/apiRecs.js'

export default {
  name: 'DashboardPage',
  components: { 
    BaseButton, 
    CourseDetailsModal, 
    MentorConnectModal, 
    CareerPathModal 
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()

    const recommendations = ref([])
    const isLoading = ref(false)
    
    // Modal states
    const isCourseModalOpen = ref(false)
    const isMentorModalOpen = ref(false)
    const isCareerModalOpen = ref(false)
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
        const { data } = await api.get(`/recommendations/${user.value.id}`)
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
    const goToProfile = () => router.push('/profile')
    const handleLogout = () => { authStore.logout(); router.push('/login') }
    
    // Modal functions
    const openCourseModal = () => { isCourseModalOpen.value = true }
    const closeCourseModal = () => { isCourseModalOpen.value = false }
    const openMentorModal = () => { isMentorModalOpen.value = true }
    const closeMentorModal = () => { isMentorModalOpen.value = false }
    const openCareerModal = () => { isCareerModalOpen.value = true }
    const closeCareerModal = () => { isCareerModalOpen.value = false }

    onMounted(() => {
      fetchRecommendations()
    })

    return {
      user,
      recommendations,
      isLoading,
      isCourseModalOpen,
      isMentorModalOpen,
      isCareerModalOpen,
      courseRecommendation,
      mentorRecommendation,
      careerRecommendation,
      goToChat,
      goToProfile,
      handleLogout,
      openCourseModal,
      closeCourseModal,
      openMentorModal,
      closeMentorModal,
      openCareerModal,
      closeCareerModal
    }
  }
}
</script>

<style scoped>
/* cards inherit the global “glass” look; spacing handled with utilities */
</style>