<!-- src/components/ai/RightPanelEmpty.vue -->
<template>
  <div class="card empty">
    <h3>✨ Ask me about your next step</h3>
    <p>Try one of these:</p>
    <ul>
      <li @click="$emit('use', 'What skills do I need for Tech Lead?')">What skills do I need for Tech Lead?</li>
      <li @click="$emit('use', 'Suggest courses for system design this quarter')">Suggest courses for system design this quarter</li>
      <li @click="$emit('use', 'Who are 3 mentors I should talk to?')">Who are 3 mentors I should talk to?</li>
    </ul>
  </div>
</template>

<style scoped>
.empty { border:1px dashed #e5e7eb; background:#fbfdff; }
ul{ margin-top:8px; padding-left:1rem; }
li{ cursor:pointer; margin:4px 0; color:#2563eb; }
li:hover{ text-decoration:underline; }
</style>