<template>
  <BaseModal :is-open="isOpen" :title="`Career Path: ${career?.title || ''}`" @close="$emit('close')">
    <div v-if="career" class="space-y-6">
      <!-- Career Header -->
      <div class="flex items-start gap-4">
        <div class="w-16 h-16 bg-green-500/20 rounded-lg flex items-center justify-center">
          <svg class="w-8 h-8 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
          </svg>
        </div>
        <div class="flex-1">
          <h3 class="text-lg font-semibold text-white">{{ career.title }}</h3>
          <p class="text-gray-300 mt-1">{{ career.description }}</p>
          <div class="flex items-center gap-4 mt-2 text-sm text-gray-400">
            <span>Match: {{ career.match_score }}%</span>
            <span>Target Role: {{ career.metadata?.target_role }}</span>
          </div>
        </div>
      </div>

      <!-- Career Timeline -->
      <div class="bg-slate-700 p-4 rounded-lg">
        <h4 class="font-medium text-white mb-4">Career Progression Timeline</h4>
        <div class="space-y-4">
          <div class="flex items-center gap-4">
            <div class="w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-medium">1</div>
            <div>
              <h5 class="font-medium text-white">Current Position</h5>
              <p class="text-sm text-gray-300">Build foundation skills</p>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <div class="w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-medium">2</div>
            <div>
              <h5 class="font-medium text-white">6-12 months</h5>
              <p class="text-sm text-gray-300">Develop specialized skills and take on more responsibility</p>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <div class="w-8 h-8 bg-green-500 text-white rounded-full flex items-center justify-center text-sm font-medium">3</div>
            <div>
              <h5 class="font-medium text-white">Target Role</h5>
              <p class="text-sm text-gray-300">{{ career.metadata?.target_role }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Required Skills -->
      <div class="bg-blue-900/30 p-4 rounded-lg border border-blue-800/50">
        <h4 class="font-medium text-blue-300 mb-3">Required Skills</h4>
        <div class="flex flex-wrap gap-2">
          <span
            v-for="skill in career.metadata?.required_skills"
            :key="skill"
            class="px-3 py-1 bg-blue-600 text-blue-100 rounded-full text-sm"
          >
            {{ skill }}
          </span>
        </div>
      </div>

      <!-- Action Plan -->
      <div class="bg-green-900/30 p-4 rounded-lg border border-green-800/50">
        <h4 class="font-medium text-green-300 mb-3">30-60-90 Day Action Plan</h4>
        <div class="space-y-3 text-sm">
          <div class="flex items-start gap-3">
            <span class="font-medium text-green-200">30 days:</span>
            <span class="text-green-100">Complete foundational courses and identify skill gaps</span>
          </div>
          <div class="flex items-start gap-3">
            <span class="font-medium text-green-200">60 days:</span>
            <span class="text-green-100">Apply new skills in current projects and seek mentorship</span>
          </div>
          <div class="flex items-start gap-3">
            <span class="font-medium text-green-200">90 days:</span>
            <span class="text-green-100">Take on stretch assignments and prepare for role transition</span>
          </div>
        </div>
      </div>

      <!-- Salary & Benefits -->
      <div class="grid gap-4 md:grid-cols-2">
        <div class="bg-slate-700 p-4 rounded-lg">
          <h4 class="font-medium text-white mb-2">Expected Salary Range</h4>
          <p class="text-lg font-semibold text-green-400">$80,000 - $120,000</p>
          <p class="text-sm text-gray-300">Based on market data and your experience level</p>
        </div>

        <div class="bg-slate-700 p-4 rounded-lg">
          <h4 class="font-medium text-white mb-2">Career Benefits</h4>
          <ul class="text-sm text-gray-300 space-y-1">
            <li>• Increased responsibility</li>
            <li>• Leadership opportunities</li>
            <li>• Higher compensation</li>
            <li>• Career advancement</li>
          </ul>
        </div>
      </div>
    </div>

    <template #footer>
      <BaseButton variant="secondary" @click="$emit('close')">Close</BaseButton>
      <BaseButton @click="startCareerPath">Start This Path</BaseButton>
    </template>
  </BaseModal>
</template>

<script>
import { defineComponent } from 'vue'
import BaseModal from '../common/BaseModal.vue'
import BaseButton from '../common/BaseButton.vue'
import { useNotifications } from '@/composables/useNotifications.js'
import { useUserActivity } from '@/composables/useUserActivity.js'

export default defineComponent({
  name: 'CareerPathModal',
  components: { BaseModal, BaseButton },
  props: {
    isOpen: {
      type: Boolean,
      default: false
    },
    career: {
      type: Object,
      default: null
    }
  },
  emits: ['close'],
  setup(props, { emit }) {
    const { showSuccess } = useNotifications()
    const { startCareerPath } = useUserActivity()
    
    const startPath = () => {
      // Start the career path
      startCareerPath(props.career)
      
      // Show success message
      showSuccess(`You have started the ${props.career?.title} career path`, 'Track your progress in your profile')
      
      // Close modal
      emit('close')
    }
    
    return {
      startCareerPath: startPath
    }
  }
})
</script>
