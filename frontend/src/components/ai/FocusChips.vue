<template>
  <div class="chips">
    <span v-for="(g,i) in (gaps||[])" :key="i" class="chip">{{ g }}</span>
  </div>
</template>
<script setup>
defineProps({ gaps: Array })
</script>
<style scoped>
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}
.chip{background:#eef2ff;color:#3730a3;border:1px solid #e0e7ff;padding:6px 10px;border-radius:999px;font-size:.82rem}
</style>