<template>
  <div class="flex flex-wrap gap-1.5">
    <button
      v-for="tag in tags"
      :key="tag.name"
      class="text-xs px-2.5 py-1 rounded-md border transition-colors cursor-pointer"
      :class="
        selected.includes(tag.name)
          ? 'bg-primary/15 border-primary/30 text-primary'
          : 'bg-base-200 border-base-content/10 text-base-content/60 hover:text-base-content hover:border-base-content/20'
      "
      @click="$emit('toggle', tag.name)"
    >
      {{ tag.name }}
      <span class="ml-1 opacity-50">{{ tag.count }}</span>
    </button>
  </div>
</template>

<script setup lang="ts">
import type { TagCount } from "../types";

defineProps<{
  tags: TagCount[];
  selected: string[];
}>();

defineEmits<{ toggle: [tag: string] }>();
</script>
