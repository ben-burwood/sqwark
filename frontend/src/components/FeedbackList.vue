<template>
    <div class="space-y-4">
        <div class="flex flex-col sm:flex-row gap-3 items-start sm:items-center">
            <SearchBar v-model="search" class="flex-1" />
            <SortToggle v-model="sort" />
        </div>

        <TagFilter v-if="allTags.length" :tags="allTags" :selected="selectedTags" @toggle="toggleTag" />

        <div v-if="loading" class="text-center py-8">
            <span class="loading loading-spinner loading-lg"></span>
        </div>

        <div v-else-if="items.length === 0" class="text-center py-8 text-base-content/50">No feedback found.</div>

        <div v-else class="space-y-3">
            <FeedbackCard v-for="item in items" :key="item.id" :feedback="item" @tag-click="toggleTag" />

            <div v-if="total > items.length" class="text-center pt-2">
                <button class="btn btn-sm btn-ghost" @click="loadMore">Load more ({{ total - items.length }} remaining)</button>
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
