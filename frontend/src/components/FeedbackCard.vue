<template>
    <div class="rounded-lg border border-base-content/10 bg-base-200 p-4 hover:border-base-content/20 transition-colors">
        <p class="text-sm leading-relaxed">{{ feedback.text }}</p>
        <div class="flex flex-wrap items-center gap-1.5 mt-3">
            <span
                v-for="tag in feedback.tags"
                :key="tag"
                class="text-[11px] px-2 py-0.5 rounded bg-base-content/5 text-base-content/50 cursor-pointer hover:text-primary hover:bg-primary/10 transition-colors"
                @click="$emit('tagClick', tag)"
            >
                {{ tag }}
            </span>
            <span class="text-[11px] text-base-content/30 ml-auto">
                {{ timeAgo(feedback.created_at) }}
            </span>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { Feedback } from "../types";

defineProps<{ feedback: Feedback }>();
defineEmits<{ tagClick: [tag: string] }>();

function timeAgo(dateStr: string): string {
    const seconds = Math.floor((Date.now() - new Date(dateStr).getTime()) / 1000);
    if (seconds < 60) return "just now";
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) return `${minutes}m ago`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours}h ago`;
    const days = Math.floor(hours / 24);
    return `${days}d ago`;
}
</script>
