<template>
    <input type="text" :value="modelValue" @input="onInput" placeholder="Search feedback..." class="input input-bordered w-full" />
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
