<script setup>
import {ref, reactive} from 'vue'
import { storeToRefs } from 'pinia'

import { useFeedingsStore } from '@/stores/feedings'
import SubmitButton from '@/components/SubmitButton.vue'
import DropDown from '@/components/DropDown.vue'
import {useUnitToggleStore} from '@/stores/unitToggle'

const unitToggleStore = useUnitToggleStore()
const feedStore = useFeedingsStore()
const { feedings } = storeToRefs(feedStore)  // reactive state
const { addFeed } = feedStore                // actions

const selectedMethod = ref('')  // define reactive ref
const required = true
const feed = ref({
  method: '',
  amount: '',
  time: '',
  notes: ''
})

const labelName = ref('Add')

const addFeedData = ()=>{
  addFeed(
    feed.value.method,
    feed.value.amount,
    feed.value.time,
    feed.value.notes)
    
  feed.value = {
    method: '',
    amount: '',
    time: '',
    notes: ''
  }
}

</script>

<template>
  <div class="w-full">
    <form @submit.prevent="addFeedData">
      <div class="grid grid-cols-1 md:grid-cols-5 gap-3 py-3 px-4 bg-gray-50 rounded-lg shadow-sm w-full">
        <!-- Method -->
        <div class="font-serif font-semibold">
          <DropDown
            v-model="feed.method"
            required = true
            name="Method"
            iconType="arrow"
            displayMode="form"
            class="w-full" 
          />
        </div>

        <!-- Amount -->
        <div class="font-serif font-semibold">
          <input
            required
            v-model="feed.amount"
            type="number"
            :placeholder="'Amount (' + unitToggleStore.unitToggle + ')'"
            class="w-full border-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 h-10 px-3"
          />
        </div>

        <!-- Time -->
        <div class="font-serif font-semibold">
          <input
            required
            v-model="feed.time"
            type="datetime-local"
            placeholder="Time"
            class="w-full border-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 h-10 px-3 text-gray-500"
          />
        </div>

        <!-- Notes -->
        <div class="font-serif font-semibold">
          <input
            v-model="feed.notes"
            placeholder="Notes"
            class="w-full border-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 h-10 px-3"
          />
        </div>

        <!-- Submit Button -->
        <div class="flex items-center">
          <SubmitButton type="submit" :label="labelName" class="w-full" />
        </div>
      </div>
    </form>
  </div>
</template>
