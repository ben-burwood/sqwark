<template>
    <div v-if="checking" class="min-h-screen bg-base-300 flex items-center justify-center">
        <span class="loading loading-spinner loading-md text-base-content/30"></span>
    </div>

    <LoginPage v-else-if="!authenticated" @authenticated="authenticated = true" />

    <div v-else class="min-h-screen bg-base-300">
        <div class="max-w-6xl mx-auto py-6 md:py-8">
            <header class="flex items-center justify-between mb-8 px-2">
                <div class="flex items-center gap-2">
                    <img src="/sqwark.svg" alt="Sqwark" class="w-8 h-8" />
                    <h1 class="text-2xl font-semibold">Sqwark</h1>
                </div>
                <div class="flex items-center gap-5">
                    <ExportButton />
                    <button @click="logout" class="btn btn-ghost btn-error btn-sm">Logout</button>
                    <ThemeToggle />
                </div>
            </header>
            <FeedbackList />
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import ExportButton from "./components/ExportButton.vue";
import FeedbackList from "./components/FeedbackList.vue";
import LoginPage from "./components/LoginPage.vue";
import ThemeToggle from "./components/ThemeToggle.vue";

const authenticated = ref(false);
const checking = ref(true);

async function checkAuth() {
    try {
        const res = await fetch("/web/tags");
        authenticated.value = res.ok;
    } catch {
        authenticated.value = false;
    } finally {
        checking.value = false;
    }
}

async function logout() {
    await fetch("/web/logout", { method: "POST" });
    authenticated.value = false;
}

onMounted(checkAuth);
</script>
