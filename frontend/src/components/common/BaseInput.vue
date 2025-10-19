<!-- src/components/common/BaseInput.vue -->
<template>
  <div class="field" :class="{ 'has-error': !!error, 'is-disabled': disabled }">
    <label v-if="label" class="label">{{ label }}</label>

    <div class="input-wrap">
      <input
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        class="input"
        @input="$emit('update:modelValue', $event.target.value)"
      />
      <span v-if="error" class="error-text">{{ error }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BaseInput',
  props: {
    modelValue: { type: [String, Number], default: '' },
    label: { type: String, default: '' },
    type: { type: String, default: 'text' },
    placeholder: { type: String, default: '' },
    error: { type: String, default: '' },
    disabled: { type: Boolean, default: false },
  },
  emits: ['update:modelValue'],
}
</script>

<style scoped>
/* Uses the same design tokens you already have; tweak values in :root for global theming */
.field { display: grid; gap: 6px; }

.label {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--muted, #6b7280);
}

.input-wrap { display: grid; gap: 6px; }

/* Core input */
.input {
  width: 100%;
  padding: 12px 14px;
  border-radius: 12px;
  border: 1px solid var(--border, rgba(0,0,0,0.1));
  background: var(--panel, #f8fafc);
  color: var(--text, #0f172a);
  font-size: 0.95rem;
  line-height: 1.4;
  transition: border-color 120ms ease, box-shadow 120ms ease, background 120ms ease;
  outline: none;
}

/* Placeholder */
.input::placeholder {
  color: color-mix(in srgb, var(--muted, #6b7280) 80%, transparent);
}

/* Hover */
.input:hover {
  border-color: color-mix(in srgb, var(--border, rgba(0,0,0,0.1)) 70%, var(--brand, #0A2463) 30%);
}

/* Focus ring (subtle brand-colored glow) */
.input:focus {
  border-color: var(--brand, #0A2463);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--brand, #0A2463) 20%, transparent);
  background: color-mix(in srgb, var(--panel, #f8fafc) 94%, white);
}

/* Error state */
.has-error .input {
  border-color: var(--danger, #ef4444);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--danger, #ef4444) 18%, transparent);
}
.error-text {
  color: var(--danger, #ef4444);
  font-size: 0.8rem;
}

/* Disabled */
.is-disabled .input {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Better autofill colors (Chrome/Safari) */
.input:-webkit-autofill,
.input:-webkit-autofill:hover,
.input:-webkit-autofill:focus {
  -webkit-text-fill-color: var(--text, #0f172a);
  transition: background-color 9999s ease-in-out 0s;
}

/* Dark-mode friendly defaults if you flip tokens later */
@media (prefers-color-scheme: dark) {
  .input {
    background: var(--panel, #0b1220);
    color: var(--text, #e5e7eb);
    border-color: var(--border, rgba(255,255,255,0.12));
  }
  .input:focus {
    background: color-mix(in srgb, var(--panel, #0b1220) 92%, black);
  }
}
</style>