<template>
  <div class="min-h-screen grid place-items-center px-4">
    <div class="w-full max-w-md card glass p-6 lg:p-8">
      <div class="text-center mb-6">
        <h1 class="text-2xl font-bold text-[var(--brand,#0A2463)]">PSA Workforce AI</h1>
        <p class="text-[var(--muted)] mt-1">Sign in to access your career dashboard</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-4">
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

        <div v-if="errors.general" class="text-red-500 text-sm">{{ errors.general }}</div>

        <BaseButton type="submit" :loading="isLoading" class="w-full">Sign In</BaseButton>
      </form>

      <div class="mt-6">
        <div class="text-center text-[var(--muted)] text-sm mb-2">Demo Accounts</div>
        <div class="rounded-lg bg-[var(--panel,#f1f5f9)] border border-white/10 p-3 text-sm leading-6">
          <div><span class="font-medium">samantha.lee@globalpsa.com</span> / demo123</div>
          <div><span class="font-medium">aisyah.rahman@globalpsa.com</span> / demo123</div>
          <div><span class="font-medium">rohan.mehta@globalpsa.com</span> / demo123</div>
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
  components: { BaseInput, BaseButton },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const email = ref('')
    const password = ref('')
    const isLoading = ref(false)
    const errors = reactive({ email: '', password: '', general: '' })

    const validateForm = () => {
      errors.email = ''
      errors.password = ''
      errors.general = ''
      if (!email.value) { errors.email = 'Email is required'; return false }
      if (!password.value) { errors.password = 'Password is required'; return false }
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
      } catch {
        errors.general = 'Login failed. Please try again.'
      } finally {
        isLoading.value = false
      }
    }

    return { email, password, isLoading, errors, handleLogin }
  }
}
</script>

<style scoped>
/* rely on shared design tokens; no inline styles */
</style>