<script setup>
	const props = defineProps({
		label: String
	})
</script>

<template>
	<button class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-6 rounded w-40 active:scale-99">{{label}}</button>
</template>