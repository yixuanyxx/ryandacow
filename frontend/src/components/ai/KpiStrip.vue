<template>
  <div class="kpis">
    <div class="kpi"><div class="v">{{ (k.fit_score||0).toFixed(1) }}%</div><div class="l">Fit</div></div>
    <div class="kpi"><div class="v">{{ (k.primary_gap_pct||0).toFixed(0) }}%</div><div class="l">Top gap</div></div>
    <div class="kpi"><div class="v">{{ k.courses_count||0 }}</div><div class="l">Courses</div></div>
  </div>
</template>
<script setup>
defineProps({ k: { type:Object, default:()=>({}) } })
</script>
<style scoped>
.kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:8px 0}
.kpi{background:#fff;border:1px solid #eee;border-radius:10px;padding:10px;text-align:center}
.v{font-weight:700}
.l{font-size:.8rem;color:#6b7280}
</style>