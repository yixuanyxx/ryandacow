<script setup>
defineProps({ gaps: { type: Array, default: () => [] } });
</script>

<template>
  <div>
    <h3 class="text-sm text-[var(--muted)] mb-2">Top gaps</h3>
    <ol class="space-y-2">
      <li
        v-for="(g, i) in gaps"
        :key="i"
        class="flex items-center justify-between bg-white/5 rounded-lg px-3 py-2"
      >
        <span class="text-sm">{{ g.skill }}</span>
        <span class="text-xs px-2 py-1 rounded-full bg-white/10"
          >{{ g.gap_score }}%</span
        >
      </li>
    </ol>
  </div>
</template>
