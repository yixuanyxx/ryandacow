<template>
  <BaseModal :is-open="isOpen" :title="`Connect with ${mentor?.title || ''}`" @close="$emit('close')">
    <div v-if="mentor" class="space-y-6">
      <!-- Mentor Header -->
      <div class="flex items-start gap-4">
        <div class="w-16 h-16 bg-purple-500/20 rounded-lg flex items-center justify-center">
          <svg class="w-8 h-8 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
          </svg>
        </div>
        <div class="flex-1">
          <h3 class="text-lg font-semibold text-white">{{ mentor.title }}</h3>
          <p class="text-gray-300 mt-1">{{ mentor.description }}</p>
          <div class="flex items-center gap-4 mt-2 text-sm text-gray-400">
            <span>Match: {{ mentor.match_score }}%</span>
            <span>{{ mentor.metadata?.job_title }}</span>
            <span>{{ mentor.metadata?.experience_years }} years experience</span>
          </div>
        </div>
      </div>

      <!-- Mentor Profile -->
      <div class="bg-slate-700 p-4 rounded-lg">
        <h4 class="font-medium text-white mb-3">Mentor Profile</h4>
        <div class="grid gap-4 md:grid-cols-2">
          <div>
            <h5 class="text-sm font-medium text-gray-300 mb-1">Current Role</h5>
            <p class="text-white">{{ mentor.metadata?.job_title }}</p>
          </div>
          <div>
            <h5 class="text-sm font-medium text-gray-300 mb-1">Department</h5>
            <p class="text-white">{{ mentor.metadata?.department }}</p>
          </div>
          <div>
            <h5 class="text-sm font-medium text-gray-300 mb-1">Experience</h5>
            <p class="text-white">{{ mentor.metadata?.experience_years }} years</p>
          </div>
          <div>
            <h5 class="text-sm font-medium text-gray-300 mb-1">Match Score</h5>
            <p class="text-white">{{ mentor.match_score }}% compatibility</p>
          </div>
        </div>
      </div>

      <!-- Expertise Areas -->
      <div class="bg-purple-900/30 p-4 rounded-lg border border-purple-800/50">
        <h4 class="font-medium text-purple-300 mb-3">Areas of Expertise</h4>
        <div class="flex flex-wrap gap-2">
          <span
            v-for="skill in mentor.metadata?.skills"
            :key="skill"
            class="px-3 py-1 bg-purple-600 text-purple-100 rounded-full text-sm"
          >
            {{ skill }}
          </span>
        </div>
      </div>

      <!-- Mentoring Style -->
      <div class="bg-blue-900/30 p-4 rounded-lg border border-blue-800/50">
        <h4 class="font-medium text-blue-300 mb-3">Mentoring Approach</h4>
        <div class="space-y-2 text-sm text-blue-200">
          <p>• <strong>Weekly 1:1 sessions:</strong> 30-45 minutes focused discussions</p>
          <p>• <strong>Goal-oriented guidance:</strong> Help you achieve specific career milestones</p>
          <p>• <strong>Practical advice:</strong> Real-world insights from industry experience</p>
          <p>• <strong>Network access:</strong> Introduction to relevant professional connections</p>
        </div>
      </div>

      <!-- Connection Form -->
      <div class="bg-slate-700 p-4 rounded-lg">
        <h4 class="font-medium text-white mb-3">Send Connection Request</h4>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">Message</label>
            <textarea
              v-model="connectionMessage"
              rows="4"
              class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Hi! I'd love to connect and learn from your experience in..."
            ></textarea>
          </div>

          <div class="grid gap-3 md:grid-cols-2">
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Preferred Meeting Time</label>
              <select
                v-model="preferredTime"
                class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Select preferred time</option>
                <option value="morning">Morning (9-12 PM)</option>
                <option value="afternoon">Afternoon (1-5 PM)</option>
                <option value="evening">Evening (6-8 PM)</option>
                <option value="flexible">Flexible</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Meeting Frequency</label>
              <select
                v-model="meetingFrequency"
                class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Select frequency</option>
                <option value="weekly">Weekly</option>
                <option value="bi-weekly">Bi-weekly</option>
                <option value="monthly">Monthly</option>
                <option value="as-needed">As needed</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <BaseButton variant="secondary" @click="$emit('close')">Cancel</BaseButton>
      <BaseButton @click="sendConnectionRequest" :disabled="!connectionMessage.trim()">Send Request</BaseButton>
    </template>
  </BaseModal>
</template>

<script>
import { ref, defineComponent } from 'vue'
import BaseModal from '../common/BaseModal.vue'
import BaseButton from '../common/BaseButton.vue'
import { useNotifications } from '@/composables/useNotifications.js'
import { useUserActivity } from '@/composables/useUserActivity.js'

export default defineComponent({
  name: 'MentorConnectModal',
  components: { BaseModal, BaseButton },
  props: {
    isOpen: {
      type: Boolean,
      default: false
    },
    mentor: {
      type: Object,
      default: null
    }
  },
  emits: ['close'],
  setup(props, { emit }) {
    const { showSuccess } = useNotifications()
    const { sendMentorRequest } = useUserActivity()
    const connectionMessage = ref('')
    const preferredTime = ref('')
    const meetingFrequency = ref('')
    
    const sendConnectionRequest = () => {
      // Send mentor request
      sendMentorRequest(props.mentor, {
        message: connectionMessage.value,
        preferredTime: preferredTime.value,
        meetingFrequency: meetingFrequency.value
      })
      
      // Show success message
      showSuccess(`Request successfully sent to ${props.mentor?.title}`)
      
      // Close modal
      emit('close')
      
      // Reset form
      connectionMessage.value = ''
      preferredTime.value = ''
      meetingFrequency.value = ''
    }
    
    return {
      connectionMessage,
      preferredTime,
      meetingFrequency,
      sendConnectionRequest
    }
  }
})
</script>
