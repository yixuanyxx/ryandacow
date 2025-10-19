<!-- views/LoginPage.vue -->
<template>
  <div class="login-container">
    <div class="login-card">
      <div class="text-center mb-6">
        <h1 style="color: #0A2463; font-size: 28px; font-weight: 700; margin-bottom: 8px;">
          PSA Workforce AI
        </h1>
        <p style="color: #64748b; font-size: 16px;">
          Sign in to access your career development dashboard
        </p>
      </div>

      <form @submit.prevent="handleLogin">
        <BaseInput
          v-model="email"
          type="email"
          label="Email"
          placeholder="Enter your email"
          :error="errors.email"
        />

        <BaseInput
          v-model="password"
          type="password"
          label="Password"
          placeholder="Enter your password"
          :error="errors.password"
        />

        <div v-if="errors.general" class="error mb-4">
          {{ errors.general }}
        </div>

        <BaseButton
          type="submit"
          :loading="isLoading"
          class="w-full"
        >
          Sign In
        </BaseButton>
      </form>

      <div class="mt-6 text-center">
        <p style="color: #94a3b8; font-size: 14px; margin-bottom: 12px;">
          Demo Accounts:
        </p>
        <div style="font-size: 12px; color: #64748b; line-height: 1.6;">
          <div>samantha.lee@globalpsa.com / demo123</div>
          <div>aisyah.rahman@globalpsa.com / demo123</div>
          <div>rohan.mehta@globalpsa.com / demo123</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth.js'
import { authService } from '@/services/authService.js'
import BaseInput from '@/components/common/BaseInput.vue'
import BaseButton from '@/components/common/BaseButton.vue'

export default {
  name: 'LoginPage',
  components: {
    BaseInput,
    BaseButton
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const email = ref('')
    const password = ref('')
    const isLoading = ref(false)
    
    const errors = reactive({
      email: '',
      password: '',
      general: ''
    })

    const validateForm = () => {
      errors.email = ''
      errors.password = ''
      errors.general = ''

      if (!email.value) {
        errors.email = 'Email is required'
        return false
      }

      if (!password.value) {
        errors.password = 'Password is required'
        return false
      }

      return true
    }

    const handleLogin = async () => {
      if (!validateForm()) return

      isLoading.value = true
      errors.general = ''

      try {
        const result = await authService.login(email.value, password.value)
        
        if (result.success) {
          authStore.login(result.user, result.token)
          router.push('/dashboard')
        } else {
          errors.general = result.error
        }
      } catch (error) {
        errors.general = 'Login failed. Please try again.'
      } finally {
        isLoading.value = false
      }
    }

    return {
      email,
      password,
      isLoading,
      errors,
      handleLogin
    }
  }
}
</script>

<style scoped>
.w-full {
  width: 100%;
}
</style>
