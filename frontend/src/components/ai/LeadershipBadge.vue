<!-- src/components/ai/LeadershipBadge.vue -->
<template>
  <div
    class="badge glass"
    :style="{ borderColor: color, color }"
    title="Leadership readiness"
  >
    <div class="row">
      <span class="dot" :style="{ background: color }" />
      <strong>{{ level }}</strong>
      <span>• {{ score.toFixed(1) }}%</span>
    </div>
    <div class="sub">Focus: {{ focus }}</div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  leadership: { type: Object, default: () => ({}) },
});

const level = computed(() => props.leadership?.level ?? "—");
const score = computed(() => Number(props.leadership?.score ?? 0));
const focus = computed(() => {
  const plan = props.leadership?.development_plan ?? [];
  const picks = plan
    .slice(0, 2)
    .map((p) => p?.skill)
    .filter(Boolean);
  return picks.length ? picks.join(", ") : "core behaviours";
});

// simple color ramp by level
const color = computed(() => {
  const lv = (level.value || "").toLowerCase();
  if (lv.includes("ready")) return "#10b981"; // green
  if (lv.includes("develop")) return "#f59e0b"; // amber
  return "#6b7280"; // gray
});
</script>

<style scoped>
.badge {
  border: 2px solid;
  border-radius: 12px;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.04);
}
.row {
  display: flex;
  align-items: center;
  gap: 8px;
}
.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
}
.sub {
  margin-top: 6px;
  font-size: 12px;
  opacity: 0.9;
}
</style>
