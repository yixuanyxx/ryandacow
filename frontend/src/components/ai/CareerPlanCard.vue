<!-- src/components/ai/CareerPlanCard.vue -->
<template>
  <div v-if="plan" class="card glass">
    <h3>🎯 {{ plan.target_role }}</h3>

    <div class="meta">
      <span>Fit score:</span>
      <strong>{{ fitPct }}%</strong>
    </div>

    <div v-if="plan.missing_skills?.length" class="block">
      <div class="label">Top gaps</div>
      <ul>
        <li v-for="(g,i) in plan.missing_skills.slice(0,3)" :key="i">
          {{ g.skill }}
          <span class="muted">({{ Number(g.gap_score ?? 0).toFixed(0) }}%)</span>
        </li>
      </ul>
    </div>

    <div v-if="plan.recommended_courses?.length" class="block">
      <div class="label">Courses</div>
      <ol>
        <li v-for="c in plan.recommended_courses" :key="c.id">
          #{{ c.id }} — {{ c.title }}
        </li>
      </ol>
    </div>

    <div v-if="plan.milestones?.length" class="block">
      <div class="label">Milestones</div>
      <ul>
        <li v-for="m in plan.milestones" :key="m.phase">
          <b>{{ m.phase }}</b>: {{ m.focus }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({ plan: { type: Object, default: () => null } })

// If backend sends 0–1, convert to percent; if already 0–100, leave as-is.
const fitPct = computed(() => {
  const s = Number(props.plan?.fit_score ?? 0)
  return (s <= 1 ? s * 100 : s).toFixed(1)
})
</script>

<style scoped>
.card {
  /* themeable “glass” card — no hard white */
  background: var(--card-bg, rgba(255,255,255,0.06));
  border: 1px solid var(--card-border, rgba(255,255,255,0.08));
  border-radius: 14px;
  padding: 16px;
  backdrop-filter: blur(8px);
}

.meta {
  display: flex;
  gap: 6px;
  align-items: center;
  margin-bottom: 8px;
}

.block { margin-top: 12px; }
.label { font-weight: 600; margin-bottom: 6px; }
.muted { color: var(--muted-fg, rgba(255,255,255,0.6)); }

/* Light-mode fallbacks (if you don’t have CSS vars set globally) */
:root {
  --card-bg: rgba(255,255,255,0.8);
  --card-border: rgba(0,0,0,0.08);
  --muted-fg: #6b7280;
}
@media (prefers-color-scheme: dark) {
  :root {
    --card-bg: rgba(255,255,255,0.06);
    --card-border: rgba(255,255,255,0.08);
    --muted-fg: rgba(255,255,255,0.65);
  }
}
</style>