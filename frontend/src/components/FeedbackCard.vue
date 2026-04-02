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
            <span class="text-[11px] text-base-content/30 ml-auto flex items-center gap-2">
                <svg
                    v-if="feedback.is_archived"
                    xmlns="http://www.w3.org/2000/svg"
                    class="w-3.5 h-3.5 text-base-content/40"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                >
                    <path d="M20.54 5.23l-1.39-1.68C18.88 3.21 18.47 3 18 3H6c-.47 0-.88.21-1.16.55L3.46 5.23C3.17 5.57 3 6.02 3 6.5V19c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V6.5c0-.48-.17-.93-.46-1.27zM12 17.5L6.5 12H10v-2h4v2h3.5L12 17.5zM5.12 5l.81-1h12l.94 1H5.12z"/>
                </svg>
                {{ timeAgo(feedback.created_at) }}
                <button
                    v-if="!feedback.is_archived"
                    class="text-base-content/20 hover:text-base-content/60 transition-colors cursor-pointer"
                    title="Archive"
                    @click.stop="$emit('archive', feedback.id)"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="21 8 21 21 3 21 3 8"/>
                        <rect x="1" y="3" width="22" height="5"/>
                        <line x1="10" y1="12" x2="14" y2="12"/>
                    </svg>
                </button>
            </span>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { Feedback } from "../types";

defineProps<{ feedback: Feedback }>();
defineEmits<{ tagClick: [tag: string]; archive: [id: string] }>();

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
