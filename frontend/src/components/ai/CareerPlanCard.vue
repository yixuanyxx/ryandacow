<!-- src/components/ai/CareerPlanCard.vue -->
<template>
  <div v-if="plan" class="card">
    <h3>🎯 {{ plan.target_role }}</h3>
    <div class="meta">
      <span>Fit score:</span>
      <strong>{{ Number(plan.fit_score ?? 0).toFixed(1) }}%</strong>
    </div>

    <div v-if="plan.missing_skills?.length" class="block">
      <div class="label">Top gaps</div>
      <ul>
        <li v-for="(g, i) in plan.missing_skills.slice(0,3)" :key="i">
          {{ g.skill }} <span class="muted">({{ Number(g.gap_score ?? 0).toFixed(0) }}%)</span>
        </li>
      </ul>
    </div>

    <div v-if="plan.recommended_courses?.length" class="block">
      <div class="label">Courses</div>
      <ol>
        <li v-for="c in plan.recommended_courses" :key="c.id">#{{ c.id }} — {{ c.title }}</li>
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
defineProps({ plan: { type: Object, default: () => null } })
</script>

<style scoped>
.card { background:#f8fafc; border:1px solid #e5e7eb; border-radius:14px; padding:16px; }
.meta { display:flex; gap:6px; align-items:center; margin-bottom:8px; }
.block { margin-top:12px; }
.label { font-weight:600; margin-bottom:6px; }
.muted { color:#6b7280; }
</style>