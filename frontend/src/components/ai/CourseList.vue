<template>
  <div class="card">
    <div class="header">Courses</div>
    <ol class="list">
      <li v-for="c in (courses || []).slice(0,3)" :key="c.id">
        <b>#{{ c.id }}</b> {{ c.title }}
      </li>
    </ol>
  </div>
</template>

<script setup>
defineProps({ courses: Array })
</script>

<style scoped>
.card{background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:12px}
.header{font-weight:600;margin-bottom:8px}
.list{padding-left:18px;display:grid;gap:4px}
</style>