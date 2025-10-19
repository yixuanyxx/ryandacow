<script setup>
import { computed } from "vue";
const props = defineProps({ value: { type: Number, default: 0 } });
const pct = computed(() => Math.max(0, Math.min(100, props.value || 0)));
</script>

<template>
  <div class="w-full">
    <div class="flex items-center justify-between mb-2">
      <h3 class="text-sm text-[var(--muted)]">Fit score</h3>
      <div class="text-sm font-semibold">{{ pct }}%</div>
    </div>
    <div class="h-3 bg-white/10 rounded-full overflow-hidden">
      <div
        class="h-full bg-gradient-to-r from-brand to-cyan-400"
        :style="{ width: pct + '%' }"
      ></div>
    </div>
  </div>
</template>
