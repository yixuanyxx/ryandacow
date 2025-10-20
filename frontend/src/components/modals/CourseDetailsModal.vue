<template>
  <BaseModal :is-open="isOpen" :title="`Course: ${course?.title || ''}`" @close="$emit('close')">
    <div v-if="course" class="space-y-6">
      <!-- Course Header -->
      <div class="flex items-start gap-4">
        <div class="w-16 h-16 bg-blue-500/20 rounded-lg flex items-center justify-center">
          <svg class="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
          </svg>
        </div>
        <div class="flex-1">
          <h3 class="text-lg font-semibold text-white">{{ course.title }}</h3>
          <p class="text-gray-300 mt-1">{{ course.description }}</p>
          <div class="flex items-center gap-4 mt-2 text-sm text-gray-400">
            <span>Match: {{ course.match_score }}%</span>
            <span>Duration: {{ course.metadata?.duration_weeks }} weeks</span>
          </div>
        </div>
      </div>

      <!-- Course Details -->
      <div class="grid gap-4 md:grid-cols-2">
        <div class="bg-slate-700 p-4 rounded-lg">
          <h4 class="font-medium text-white mb-2">What You'll Learn</h4>
          <ul class="text-sm text-gray-300 space-y-1">
            <li v-for="skill in course.metadata?.required_skills" :key="skill">• {{ skill }}</li>
          </ul>
        </div>
        
        <div class="bg-slate-700 p-4 rounded-lg">
          <h4 class="font-medium text-white mb-2">Course Format</h4>
          <div class="text-sm text-gray-300 space-y-1">
            <p>• Self-paced online learning</p>
            <p>• Interactive exercises</p>
            <p>• Certificate upon completion</p>
            <p>• Lifetime access to materials</p>
          </div>
        </div>
      </div>

      <!-- Learning Path -->
      <div class="bg-blue-900/30 p-4 rounded-lg border border-blue-800/50">
        <h4 class="font-medium text-blue-300 mb-3">Learning Path</h4>
        <div class="space-y-2 text-sm text-blue-200">
          <div class="flex items-center gap-2">
            <span class="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center text-xs font-medium text-white">1</span>
            <span>Foundation concepts and theory</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center text-xs font-medium text-white">2</span>
            <span>Hands-on practice and exercises</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center text-xs font-medium text-white">3</span>
            <span>Real-world project application</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center text-xs font-medium text-white">4</span>
            <span>Assessment and certification</span>
          </div>
        </div>
      </div>

      <!-- Prerequisites -->
      <div v-if="course.metadata?.prerequisites" class="bg-yellow-900/30 p-4 rounded-lg border border-yellow-800/50">
        <h4 class="font-medium text-yellow-300 mb-2">Prerequisites</h4>
        <p class="text-sm text-yellow-200">{{ course.metadata?.prerequisites }}</p>
      </div>
    </div>

    <template #footer>
      <BaseButton variant="secondary" @click="$emit('close')">Close</BaseButton>
      <BaseButton @click="enrollCourse">Enroll Now</BaseButton>
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
  name: 'CourseDetailsModal',
  components: { BaseModal, BaseButton },
  props: {
    isOpen: {
      type: Boolean,
      default: false
    },
    course: {
      type: Object,
      default: null
    }
  },
  emits: ['close'],
  setup(props, { emit }) {
    const { showSuccess } = useNotifications()
    const { enrollInCourse } = useUserActivity()
    
    const enrollCourse = () => {
      // Enroll in the course
      enrollInCourse(props.course)
      
      // Show success message
      showSuccess(`You have successfully enrolled into ${props.course?.title}`)
      
      // Close modal
      emit('close')
    }
    
    return {
      enrollCourse
    }
  }
})
</script>
