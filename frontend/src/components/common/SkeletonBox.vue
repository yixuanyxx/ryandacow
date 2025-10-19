<!-- src/components/common/SkeletonBox.vue -->
<template><div class="skel glass" /></template>
<style scoped>
.skel {
  height: 120px;
  border-radius: 12px;
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0.05),
    rgba(255, 255, 255, 0.08),
    rgba(255, 255, 255, 0.05)
  );
  background-size: 200% 100%;
  animation: shimmer 1.2s infinite;
  border: 1px solid rgba(255, 255, 255, 0.08);
}
@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
</style>
