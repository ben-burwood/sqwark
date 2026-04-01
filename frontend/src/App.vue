<template>
    <div class="min-h-screen bg-base-300">
        <div class="max-w-6xl mx-auto py-6 md:py-8">
            <header class="flex items-center justify-between mb-8 px-2">
                <div>
                    <h1 class="text-2xl font-semibold">Sqwark</h1>
                </div>
                <div class="flex items-center gap-5">
                    <ExportButton />
                    <ThemeToggle />
                </div>
            </header>
            <FeedbackList />
        </div>
    </div>
</template>

<script setup lang="ts">
import ExportButton from "./components/ExportButton.vue";
import FeedbackList from "./components/FeedbackList.vue";
import ThemeToggle from "./components/ThemeToggle.vue";
</script>
