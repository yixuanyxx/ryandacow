<!-- src/components/common/SkeletonBox.vue -->
<template><div class="skel" /></template>
<style scoped>
.skel{
  height: 120px; border-radius:12px; background:linear-gradient(90deg,#f3f4f6,#eceff1,#f3f4f6);
  background-size:200% 100%; animation:shimmer 1.2s infinite;
}
@keyframes shimmer{0%{background-position:200% 0}100%{background-position:-200% 0}}
</style>