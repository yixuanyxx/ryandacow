<template>
  <div v-html="safeHtml" />
</template>

<script setup>
import { computed } from "vue";
import { marked } from "marked";
import DOMPurify from "dompurify";

const props = defineProps({ text: { type: String, default: "" } });
const safeHtml = computed(() => {
  const html = marked.parse(props.text || "");
  return DOMPurify.sanitize(html);
});
</script>

<style scoped>
:deep(h2) {
  font-size: 1rem;
  margin: 6px 0 4px;
}
:deep(ul) {
  padding-left: 1.1rem;
  margin: 6px 0;
}
:deep(li) {
  margin: 2px 0;
}
:deep(b),
:deep(strong) {
  font-weight: 600;
}
</style>