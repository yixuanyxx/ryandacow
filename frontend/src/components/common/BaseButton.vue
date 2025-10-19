<!-- components/common/BaseButton.vue -->
<template>
  <button 
    :class="buttonClass" 
    :disabled="disabled || loading"
    @click="$emit('click')"
  >
    <span v-if="loading">Loading...</span>
    <span v-else><slot /></span>
  </button>
</template>

<script>
export default {
  name: 'BaseButton',
  props: {
    variant: {
      type: String,
      default: 'primary',
      validator: (value) => ['primary', 'secondary'].includes(value)
    },
    disabled: {
      type: Boolean,
      default: false
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  emits: ['click'],
  computed: {
    buttonClass() {
      const baseClass = 'btn'
      const variantClass = this.variant === 'secondary' ? 'btn-secondary' : ''
      const disabledClass = (this.disabled || this.loading) ? 'loading' : ''
      return [baseClass, variantClass, disabledClass].filter(Boolean).join(' ')
    }
  }
}
</script>
