<template>
    <div class="flex flex-wrap gap-2">
        <button
            v-for="tag in tags"
            :key="tag.name"
            class="badge badge-lg cursor-pointer"
            :class="selected.includes(tag.name) ? 'badge-primary' : 'badge-outline'"
            @click="$emit('toggle', tag.name)"
        >
            {{ tag.name }}
            <span class="ml-1 opacity-60">{{ tag.count }}</span>
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
