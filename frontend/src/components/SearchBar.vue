<template>
  <div class="relative">
    <svg
      class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-base-content/30"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      stroke-width="2"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
      />
    </svg>
    <input
      type="text"
      :value="modelValue"
      @input="onInput"
      placeholder="Search feedback..."
      class="input input-sm input-bordered w-full pl-9 bg-base-200 border-base-content/10 focus:border-base-content/20 focus:outline-none text-sm"
    />
  </div>
</template>

<script setup lang="ts">
let timer: ReturnType<typeof setTimeout>;

const props = defineProps<{ modelValue: string }>();
const emit = defineEmits<{ "update:modelValue": [value: string] }>();

function onInput(e: Event) {
  const value = (e.target as HTMLInputElement).value;
  clearTimeout(timer);
  timer = setTimeout(() => emit("update:modelValue", value), 300);
}
</script>
