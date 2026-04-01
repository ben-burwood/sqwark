<template>
    <div class="space-y-4">
        <div class="rounded-lg border border-base-content/10 bg-base-200 p-4">
            <div class="flex flex-col sm:flex-row gap-3 items-start sm:items-center">
                <SearchBar v-model="search" class="flex-1 w-full" />
                <SortToggle v-model="sort" />
            </div>
            <TagFilter v-if="allTags.length" :tags="allTags" :selected="selectedTags" @toggle="toggleTag" class="mt-3" />
        </div>

        <div class="text-xs text-base-content/40 px-1">
            <span>{{ total }} feedback{{ total !== 1 ? 's' : '' }}</span>
        </div>

        <div v-if="loading" class="flex justify-center py-16">
            <span class="loading loading-spinner loading-md text-base-content/30"></span>
        </div>

        <div v-else-if="items.length === 0" class="text-center py-16 text-sm text-base-content/30">
            No feedback found.
        </div>

        <div v-else class="space-y-2">
            <FeedbackCard v-for="item in items" :key="item.id" :feedback="item" @tag-click="toggleTag" />

            <div v-if="total > items.length" class="text-center pt-4">
                <button
                    class="text-xs px-4 py-2 rounded-lg border border-base-content/10 text-base-content/50 hover:text-base-content hover:border-base-content/20 transition-colors cursor-pointer"
                    @click="loadMore"
                >
                    Load more ({{ total - items.length }} remaining)
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from "vue";
import type { Feedback, TagCount } from "../types";
import SearchBar from "./SearchBar.vue";
import SortToggle from "./SortToggle.vue";
import TagFilter from "./TagFilter.vue";
import FeedbackCard from "./FeedbackCard.vue";

const search = ref("");
const sort = ref<"newest" | "oldest">("newest");
const selectedTags = ref<string[]>([]);
const items = ref<Feedback[]>([]);
const total = ref(0);
const allTags = ref<TagCount[]>([]);
const loading = ref(true);

const PAGE_SIZE = 50;

function toggleTag(tag: string) {
    const idx = selectedTags.value.indexOf(tag);
    if (idx >= 0) {
        selectedTags.value.splice(idx, 1);
    } else {
        selectedTags.value.push(tag);
    }
}

async function fetchFeedback(append = false) {
    loading.value = !append;
    const url = new URL("/web/feedback", window.location.origin);
    if (search.value) url.searchParams.set("search", search.value);
    url.searchParams.set("sort", sort.value);
    if (selectedTags.value.length) url.searchParams.set("tag", selectedTags.value.join(","));
    url.searchParams.set("limit", String(PAGE_SIZE));
    if (append) url.searchParams.set("offset", String(items.value.length));

    const res = await fetch(url);
    const result = await res.json();

    if (append) {
        items.value.push(...result.items);
    } else {
        items.value = result.items;
    }
    total.value = result.total;
    loading.value = false;
}

function loadMore() {
    fetchFeedback(true);
}

async function fetchTags() {
    const res = await fetch("/web/tags");
    const data = await res.json();
    allTags.value = data.tags;
}

watch([search, sort, selectedTags], () => fetchFeedback(), { deep: true });

onMounted(() => {
    fetchFeedback();
    fetchTags();
});
</script>
