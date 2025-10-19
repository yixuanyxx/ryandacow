<!-- src/components/ai/RightPanelEmpty.vue -->
<template>
  <div class="card glass p-4">
    <h3 class="text-lg font-semibold mb-1">✨ Ask me about your next step</h3>
    <p class="text-sm text-[var(--muted)] mb-3">
      Try one of these to get started:
    </p>
    <div class="flex flex-wrap gap-2">
      <button
        class="px-3 py-1 rounded-full text-sm border border-transparent bg-gradient-to-r from-brand/20 to-cyan-400/20 hover:from-brand/30 hover:to-cyan-400/30 transition"
        @click="$emit('use', 'What skills do I need for Tech Lead?')"
      >
        Tech Lead skills
      </button>
      <button
        class="px-3 py-1 rounded-full text-sm border border-transparent bg-gradient-to-r from-brand/20 to-cyan-400/20 hover:from-brand/30 hover:to-cyan-400/30 transition"
        @click="$emit('use', 'Suggest courses for system design this quarter')"
      >
        System design courses
      </button>
      <button
        class="px-3 py-1 rounded-full text-sm border border-transparent bg-gradient-to-r from-brand/20 to-cyan-400/20 hover:from-brand/30 hover:to-cyan-400/30 transition"
        @click="$emit('use', 'Who are 3 mentors I should talk to?')"
      >
        Find mentors
      </button>
      <button
        class="px-3 py-1 rounded-full text-sm border border-transparent bg-gradient-to-r from-brand/20 to-cyan-400/20 hover:from-brand/30 hover:to-cyan-400/30 transition"
        @click="$emit('use', 'Create a 30-60-90 day plan for Tech Lead')"
      >
        30-60-90 plan
      </button>
    </div>
  </div>
</template>
