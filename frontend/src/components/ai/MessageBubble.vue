<template>
  <div :class="['mb-3', mine ? 'text-right' : 'text-left']">
    <div
      :class="[
        'inline-block max-w-[72ch] px-4 py-3 rounded-2xl shadow-soft',
        mine
          ? 'bg-gradient-to-br from-brand/90 to-brand-2/70 text-white rounded-br-sm'
          : 'bg-[var(--card)]/90 border border-white/10 rounded-bl-sm',
      ]"
    >
      <slot />
    </div>
  </div>
</template>
<script setup>
defineProps({ mine: Boolean });
</script>
