<template>
  <div class="min-h-screen bg-slate-900">
    <div class="container mx-auto px-4 py-8">
      <!-- Header -->
      <div class="flex items-center justify-between mb-8">
        <div class="flex items-center gap-4">
          <BaseButton variant="secondary" @click="goBack">Back</BaseButton>
          <h1 class="text-2xl font-bold text-white">Profile</h1>
        </div>
        <div class="flex items-center gap-4">
          <BaseButton variant="secondary" @click="handleLogout">Logout</BaseButton>
        </div>
      </div>

      <div class="grid gap-6 lg:grid-cols-3">
        <!-- Profile Information -->
        <div class="lg:col-span-2">
          <div class="card glass p-6">
            <h2 class="text-xl font-semibold mb-4 text-white">Personal Information</h2>
            
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Full Name</label>
                <BaseInput 
                  v-model="profile.name" 
                  placeholder="Enter your full name"
                  :disabled="!isEditing"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Job Title</label>
                <BaseInput 
                  v-model="profile.job_title" 
                  placeholder="Enter your job title"
                  :disabled="!isEditing"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Department</label>
                <BaseInput 
                  v-model="profile.department" 
                  placeholder="Enter your department"
                  :disabled="!isEditing"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Email</label>
                <BaseInput 
                  v-model="profile.email" 
                  type="email"
                  placeholder="Enter your email"
                  :disabled="!isEditing"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Career Goal</label>
                <BaseInput 
                  v-model="profile.career_goal" 
                  placeholder="Describe your career aspirations"
                  :disabled="!isEditing"
                />
              </div>
            </div>
            
            <div class="flex gap-3 mt-6">
              <BaseButton v-if="!isEditing" @click="startEditing">Edit Profile</BaseButton>
              <BaseButton v-if="isEditing" @click="saveProfile" variant="primary">Save Changes</BaseButton>
              <BaseButton v-if="isEditing" @click="cancelEditing" variant="secondary">Cancel</BaseButton>
            </div>
          </div>
        </div>

        <!-- Skills & Preferences -->
        <div class="space-y-6">
          <!-- Skills -->
          <div class="card glass p-6">
            <h3 class="text-lg font-semibold mb-4 text-white">Skills</h3>
            <div class="space-y-2">
              <div v-for="skill in profile.skills" :key="skill" class="flex items-center justify-between">
                <span class="text-sm text-gray-300">{{ skill }}</span>
                <BaseButton size="small" variant="secondary" @click="removeSkill(skill)">Remove</BaseButton>
              </div>
              <div class="flex gap-2 mt-3">
                <BaseInput 
                  v-model="newSkill" 
                  placeholder="Add skill"
                  size="small"
                />
                <BaseButton size="small" @click="addSkill" :disabled="!newSkill.trim()">Add</BaseButton>
              </div>
            </div>
          </div>

          <!-- Preferences -->
          <div class="card glass p-6">
            <h3 class="text-lg font-semibold mb-4 text-white">Preferences</h3>
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-300">Email Notifications</span>
                <input 
                  type="checkbox" 
                  v-model="preferences.emailNotifications"
                  class="rounded border-gray-600 bg-slate-800 text-blue-600"
                />
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-300">Weekly Career Tips</span>
                <input 
                  type="checkbox" 
                  v-model="preferences.weeklyTips"
                  class="rounded border-gray-600 bg-slate-800 text-blue-600"
                />
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-300">Mentor Matching</span>
                <input 
                  type="checkbox" 
                  v-model="preferences.mentorMatching"
                  class="rounded border-gray-600 bg-slate-800 text-blue-600"
                />
              </div>
            </div>
            <BaseButton @click="savePreferences" class="mt-4" size="small">Save Preferences</BaseButton>
          </div>

          <!-- My Activities -->
          <div class="card glass p-6">
            <h3 class="text-lg font-semibold mb-4 text-white">My Activities</h3>
            
            <!-- Clear All Button -->
            <div v-if="hasAnyActivities" class="mb-4 flex justify-end">
              <BaseButton 
                variant="secondary" 
                size="small" 
                @click="showClearConfirm = true"
                class="text-red-400 hover:text-red-300 hover:bg-red-900/20"
              >
                Clear All Activities
              </BaseButton>
            </div>
            
            <!-- Enrolled Courses -->
            <div v-if="enrolledCourses.length > 0" class="mb-6">
              <h4 class="text-md font-medium text-gray-300 mb-3">Enrolled Courses</h4>
              <div class="space-y-3">
                <div v-for="course in enrolledCourses" :key="course.id" class="bg-blue-900/30 p-3 rounded-lg border border-blue-800/50">
                  <div class="flex items-center justify-between">
                    <div>
                      <h5 class="font-medium text-white">{{ course.title }}</h5>
                      <p class="text-sm text-gray-300">Enrolled {{ formatDate(course.enrolledAt) }}</p>
                    </div>
                    <div class="text-right">
                      <div class="text-sm font-medium text-blue-400">{{ course.progress }}% Complete</div>
                      <div class="w-20 bg-gray-600 rounded-full h-2 mt-1">
                        <div class="bg-blue-500 h-2 rounded-full" :style="{ width: course.progress + '%' }"></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Mentor Requests -->
            <div v-if="mentorRequests.length > 0" class="mb-6">
              <h4 class="text-md font-medium text-gray-300 mb-3">Mentor Requests</h4>
              <div class="space-y-3">
                <div v-for="request in mentorRequests" :key="request.id" class="bg-purple-900/30 p-3 rounded-lg border border-purple-800/50">
                  <div class="flex items-center justify-between">
                    <div>
                      <h5 class="font-medium text-white">{{ request.mentorName }}</h5>
                      <p class="text-sm text-gray-300">Sent {{ formatDate(request.sentAt) }}</p>
                      <p class="text-sm text-gray-400">{{ request.message }}</p>
                    </div>
                    <div class="text-right">
                      <span :class="getStatusClass(request.status)" class="px-2 py-1 rounded-full text-xs font-medium">
                        {{ request.status }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Started Career Paths -->
            <div v-if="startedPaths.length > 0" class="mb-6">
              <h4 class="text-md font-medium text-gray-300 mb-3">Career Paths</h4>
              <div class="space-y-3">
                <div v-for="path in startedPaths" :key="path.id" class="bg-green-900/30 p-3 rounded-lg border border-green-800/50">
                  <div class="flex items-center justify-between mb-2">
                    <div>
                      <h5 class="font-medium text-white">{{ path.title }}</h5>
                      <p class="text-sm text-gray-300">Started {{ formatDate(path.startedAt) }}</p>
                    </div>
                    <div class="text-right">
                      <div class="text-sm font-medium text-green-400">{{ path.progress }}% Complete</div>
                      <div class="w-20 bg-gray-600 rounded-full h-2 mt-1">
                        <div class="bg-green-500 h-2 rounded-full" :style="{ width: path.progress + '%' }"></div>
                      </div>
                    </div>
                  </div>
                  <div class="space-y-1">
                    <div v-for="(milestone, index) in path.milestones" :key="index" class="flex items-center gap-2 text-sm">
                      <div :class="milestone.completed ? 'bg-green-500' : 'bg-gray-600'" class="w-4 h-4 rounded-full flex items-center justify-center">
                        <svg v-if="milestone.completed" class="w-2 h-2 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                        </svg>
                      </div>
                      <span :class="milestone.completed ? 'text-green-300' : 'text-gray-300'">
                        {{ milestone.phase }}: {{ milestone.focus }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="enrolledCourses.length === 0 && mentorRequests.length === 0 && startedPaths.length === 0" class="text-center py-8">
              <div class="text-gray-400 mb-2">
                <svg class="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <p class="text-gray-500">No activities yet</p>
              <p class="text-sm text-gray-400">Start by enrolling in courses or connecting with mentors</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Clear All Activities Confirmation Modal -->
    <div v-if="showClearConfirm" class="fixed inset-0 z-50 flex items-center justify-center">
      <!-- Backdrop -->
      <div
        class="absolute inset-0 bg-black bg-opacity-50"
        @click="showClearConfirm = false"
      ></div>

      <!-- Modal -->
      <div class="relative bg-slate-800 rounded-lg shadow-xl max-w-md w-full mx-4 border border-slate-700">
        <!-- Header -->
        <div class="flex items-center justify-between p-6 border-b border-slate-700">
          <h2 class="text-xl font-semibold text-white">Clear All Activities</h2>
          <button
            @click="showClearConfirm = false"
            class="text-gray-400 hover:text-gray-200"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <!-- Content -->
        <div class="p-6">
          <div class="flex items-start gap-4">
            <div class="w-12 h-12 bg-red-500/20 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
              </svg>
            </div>
            <div class="flex-1">
              <h3 class="text-lg font-semibold text-white mb-2">Are you sure?</h3>
              <p class="text-gray-300 mb-4">
                This will permanently delete all your enrolled courses, mentor requests, and started career paths. This action cannot be undone.
              </p>
              <div class="bg-red-900/30 p-3 rounded-lg border border-red-800/50">
                <p class="text-sm text-red-200">
                  <strong>This will remove:</strong><br>
                  • {{ enrolledCourses.length }} enrolled course(s)<br>
                  • {{ mentorRequests.length }} mentor request(s)<br>
                  • {{ startedPaths.length }} career path(s)
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="flex items-center justify-end gap-3 p-6 border-t border-slate-700">
          <BaseButton variant="secondary" @click="showClearConfirm = false">Cancel</BaseButton>
          <BaseButton 
            @click="clearAllActivities" 
            class="bg-red-600 hover:bg-red-700 text-white"
          >
            Clear All Activities
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
import BaseInput from '@/components/common/BaseInput.vue'
import { useUserActivity } from '@/composables/useUserActivity.js'

export default {
  name: 'ProfilePage',
  components: { BaseButton, BaseInput },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const { enrolledCourses, mentorRequests, startedPaths, clearAllActivities: clearActivities } = useUserActivity()
    
    const isEditing = ref(false)
    const newSkill = ref('')
    const showClearConfirm = ref(false)
    
    const profile = ref({
      name: '',
      job_title: '',
      department: '',
      email: '',
      career_goal: '',
      skills: []
    })
    
    const preferences = ref({
      emailNotifications: true,
      weeklyTips: true,
      mentorMatching: false
    })
    
    const user = computed(() => authStore.user)
    
    // Computed property to check if user has any activities
    const hasAnyActivities = computed(() => {
      return enrolledCourses.value.length > 0 || 
             mentorRequests.value.length > 0 || 
             startedPaths.value.length > 0
    })
    
    const startEditing = () => {
      isEditing.value = true
    }
    
    const cancelEditing = () => {
      isEditing.value = false
      // Reset profile to original values
      loadProfile()
    }
    
    const saveProfile = () => {
      // Here you would typically save to backend
      console.log('Saving profile:', profile.value)
      isEditing.value = false
      // Show success message
    }
    
    const addSkill = () => {
      if (newSkill.value.trim()) {
        profile.value.skills.push(newSkill.value.trim())
        newSkill.value = ''
      }
    }
    
    const removeSkill = (skill) => {
      const index = profile.value.skills.indexOf(skill)
      if (index > -1) {
        profile.value.skills.splice(index, 1)
      }
    }
    
    const savePreferences = () => {
      // Here you would typically save to backend
      console.log('Saving preferences:', preferences.value)
      // Show success message
    }
    
    const clearAllActivities = () => {
      // Clear all activities using the composable function
      clearActivities()
      
      // Close the confirmation modal
      showClearConfirm.value = false
      
      // Show success message
      console.log('All activities cleared successfully')
    }
    
    const loadProfile = () => {
      if (user.value) {
        profile.value = {
          name: user.value.name || '',
          job_title: user.value.job_title || '',
          department: user.value.department || '',
          email: user.value.email || '',
          career_goal: `Senior ${user.value.job_title || 'Professional'} (2-3 years)`,
          skills: ['Python', 'System Design', 'Leadership', 'Project Management']
        }
      }
    }
    
    const goBack = () => router.push('/dashboard')
    const handleLogout = () => { 
      authStore.logout()
      router.push('/login')
    }
    
    // Helper functions
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
      })
    }
    
    const getStatusClass = (status) => {
      switch (status) {
        case 'pending':
          return 'bg-yellow-100 text-yellow-800'
        case 'accepted':
          return 'bg-green-100 text-green-800'
        case 'rejected':
          return 'bg-red-100 text-red-800'
        default:
          return 'bg-gray-100 text-gray-800'
      }
    }
    
    onMounted(() => {
      loadProfile()
    })
    
    return {
      profile,
      preferences,
      isEditing,
      newSkill,
      showClearConfirm,
      hasAnyActivities,
      user,
      enrolledCourses,
      mentorRequests,
      startedPaths,
      startEditing,
      cancelEditing,
      saveProfile,
      addSkill,
      removeSkill,
      savePreferences,
      clearAllActivities,
      goBack,
      handleLogout,
      formatDate,
      getStatusClass
    }
  }
}
</script>

<style scoped>
.card {
  background: var(--card-bg, rgba(255,255,255,0.06));
  border: 1px solid var(--card-border, rgba(255,255,255,0.08));
  border-radius: 14px;
  backdrop-filter: blur(8px);
}

.glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}
</style>
