<template>
    <div class="join">
        <button class="btn btn-sm join-item" :class="modelValue === 'newest' ? 'btn-active' : ''" @click="$emit('update:modelValue', 'newest')">
            Newest
        </button>
        <button class="btn btn-sm join-item" :class="modelValue === 'oldest' ? 'btn-active' : ''" @click="$emit('update:modelValue', 'oldest')">
            Oldest
        </button>
    </div>
</template>

<script setup lang="ts">
defineProps<{ modelValue: "newest" | "oldest" }>();
defineEmits<{ "update:modelValue": [value: "newest" | "oldest"] }>();
</script>
