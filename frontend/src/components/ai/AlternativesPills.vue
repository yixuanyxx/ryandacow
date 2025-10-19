<template>
  <div v-if="(alternatives||[]).length" class="wrap">
    <span class="label">Alternatives:</span>
    <span v-for="a in alternatives" :key="a.role_id" class="pill">{{ a.role }}</span>
  </div>
</template>

<script setup>
defineProps({ alternatives: Array })
</script>

<style scoped>
.wrap{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.label{color:#6b7280}
.pill{background:#eef2ff;color:#3730a3;border-radius:999px;padding:4px 10px;font-size:.85rem}
</style>