<template>
  <div class="flex rounded-lg border border-base-content/10 overflow-hidden">
    <button
      class="text-xs px-3 py-1.5 transition-colors cursor-pointer"
      :class="
        modelValue === 'newest'
          ? 'bg-base-content/10 text-base-content'
          : 'text-base-content/50 hover:text-base-content'
      "
      @click="$emit('update:modelValue', 'newest')"
    >
      Newest
    </button>
    <button
      class="text-xs px-3 py-1.5 transition-colors cursor-pointer border-l border-base-content/10"
      :class="
        modelValue === 'oldest'
          ? 'bg-base-content/10 text-base-content'
          : 'text-base-content/50 hover:text-base-content'
      "
      @click="$emit('update:modelValue', 'oldest')"
    >
      Oldest
    </button>
  </div>
</template>

<script setup lang="ts">
defineProps<{ modelValue: "newest" | "oldest" }>();
defineEmits<{ "update:modelValue": [value: "newest" | "oldest"] }>();
</script>
