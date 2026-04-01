<template>
    <div class="card bg-base-100 shadow-sm">
        <div class="card-body p-4">
            <p class="text-base">{{ feedback.text }}</p>
            <div class="flex flex-wrap items-center gap-2 mt-2">
                <span
                    v-for="tag in feedback.tags"
                    :key="tag"
                    class="badge badge-sm badge-outline cursor-pointer hover:badge-primary"
                    @click="$emit('tagClick', tag)"
                >
                    {{ tag }}
                </span>
                <span class="text-xs text-base-content/50 ml-auto">
                    {{ timeAgo(feedback.created_at) }}
                </span>
            </div>
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
