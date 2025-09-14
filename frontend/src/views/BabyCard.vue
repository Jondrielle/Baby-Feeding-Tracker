<script setup>
import {ref,reactive} from 'vue'
import FeedingForm from '@/components/FeedingForm.vue'
import FeedingTable from '@/components/FeedingTable.vue'

</script>

<template>
  <div>
    <header class="font-serif font-bold text-xl mb-4">Feeding Log</header>
    <div class="flex flex-col items-center">
      <FeedingForm/>
      <FeedingTable/>
    </div>
  </div>
</template>