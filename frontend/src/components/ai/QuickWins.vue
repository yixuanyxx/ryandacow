<script setup>
const emit = defineEmits(["send"]);
const actions = [
  "Create a 30-60-90 for Tech Lead",
  "Suggest 3 courses to close my top gaps",
  "Who are 3 mentors to talk to this month?",
];
</script>

<template>
  <div>
    <h3 class="text-sm text-[var(--muted)] mb-2">Quick wins</h3>
    <div class="flex flex-wrap gap-2">
      <button
        v-for="(a, i) in actions"
        :key="i"
        class="px-3 py-1 rounded-full text-sm bg-gradient-to-r from-white/10 to-white/5 border border-white/10 hover:border-brand/40 transition"
        @click="emit('send', a)"
      >
        {{ a }}
      </button>
    </div>
  </div>
</template>
