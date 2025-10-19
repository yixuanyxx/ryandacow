<template>
  <div class="card" v-if="mentor">
    <div class="row">
      <div>
        <div class="t">Mentor to contact</div>
        <div class="n">{{ mentor.name }}</div>
      </div>
      <button class="btn" @click="copy">Copy DM</button>
    </div>
  </div>
</template>
<script setup>
const props = defineProps({ mentor:Object, role:String })
const copy = () => {
  const msg = `Hi ${props.mentor?.name}, could I book a 20-min 1:1 to discuss steps toward ${props.role}?`
  navigator.clipboard.writeText(msg)
}
</script>
<style scoped>
.card{border:1px solid #eee;background:#fff;border-radius:12px;padding:12px}
.row{display:flex;align-items:center;justify-content:space-between}
.t{font-size:.8rem;color:#6b7280}
.n{font-weight:600}
.btn{border:1px solid #e5e7eb;background:#f9fafb;border-radius:8px;padding:6px 10px}
.btn:hover{background:#f3f4f6}
</style>