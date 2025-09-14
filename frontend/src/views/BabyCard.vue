<script setup>
import {ref,reactive} from 'vue'
import FeedingForm from '@/components/FeedingForm.vue'
import FeedingTable from '@/components/FeedingTable.vue'

</script>

<template>
  <div class="flex flex-col mt-10 w-full max-w-4xl mx-auto p-6 border rounded-lg shadow-md bg-white">
    <!-- Header -->
    <header class="font-serif font-bold text-2xl mb-6 w-full text-left">
      Feeding Log
    </header>

    <!-- Form and Table -->
    <div class="flex flex-col items-center gap-6 w-full">
      <!-- Feeding Form -->
      <div class="w-full">
        <FeedingForm />
      </div>

      <!-- Feeding Table -->
      <div class="w-full overflow-x-auto">
        <FeedingTable />
      </div>
    </div>
  </div>
</template>
