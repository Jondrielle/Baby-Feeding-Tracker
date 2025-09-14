<script setup>
import {ref,reactive} from 'vue'
import FeedingForm from '@/components/FeedingForm.vue'
import FeedingTable from '@/components/FeedingTable.vue'

const feedings = ref([])

const addFeeding = (feed)=> {
  feedings.value.push(feed)
  console.log(feed)
}

</script>

<template>
  <div>
    <header class="font-serif font-bold text-xl mb-4">Feeding Log</header>
    <div class="flex flex-col items-center">
      <FeedingForm @add-feeding="addFeeding" class="mb=30"/>
      <FeedingTable :tablefeeds="feedings"/>
    </div>
  </div>
</template>