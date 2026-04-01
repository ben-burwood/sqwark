<template>
    <LoginPage v-if="!authenticated" @authenticated="authenticated = true" />
    <div v-else class="min-h-screen bg-base-300">
        <div class="max-w-6xl mx-auto py-6 md:py-8">
            <header class="flex items-center justify-between mb-8 px-2">
                <div>
                    <h1 class="text-2xl font-semibold">Sqwark</h1>
                </div>
                <div class="flex items-center gap-5">
                    <ExportButton />
                    <button @click="logout" class="text-xs text-base-content/40 hover:text-base-content transition-colors cursor-pointer">
                        Logout
                    </button>
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

async function checkAuth() {
    try {
        const res = await fetch("/web/tags");
        authenticated.value = res.ok;
    } catch {
        authenticated.value = false;
    }
}

async function logout() {
    await fetch("/web/logout", { method: "POST" });
    authenticated.value = false;
}

onMounted(checkAuth);
</script>
