<template>
  <div class="card">
    <div class="header">🧭 Mentors</div>
    <ul class="list">
      <li v-for="m in (mentors || []).slice(0,3)" :key="m.id">
        {{ m.name }} <span class="muted">(ID: {{ m.id }})</span>
      </li>
    </ul>
  </div>
</template>

<script setup>
defineProps({ mentors: Array })
</script>

<style scoped>
.card{background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:12px}
.header{font-weight:600;margin-bottom:8px}
.list{display:grid;gap:4px;padding-left:18px}
.muted{color:#6b7280}
</style>