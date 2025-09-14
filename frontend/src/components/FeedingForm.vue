<script setup>
import {ref, reactive} from 'vue'
import { storeToRefs } from 'pinia'

import { useFeedingsStore } from '@/stores/feedings'
import SubmitButton from '@/components/SubmitButton.vue'
import DropDown from '@/components/DropDown.vue'

const feedStore = useFeedingsStore()
const { feedings } = storeToRefs(feedStore)  // reactive state
const { addFeed } = feedStore                // actions

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
  <div class="grid grid-cols-5 gap-2 py-3 px-4">
    <div class="font-serif font-semibold">
      <DropDown name="Method" :required="true" v-model="feed.method" class="w-full"/>
    </div>
    <div class="font-serif font-semibold">
      <input v-model="feed.amount" required type="number" placeholder="Amount" class="w-full border-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 h-10 px-3"></input>
    </div>
    <div class="font-serif font-semibold">
      <input v-model="feed.time" required type="datetime-local" placeholder="Time" class="w-full border-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 px-3 text-[#8e8e8e] h-10"></input>
    </div>
    <div class="font-serif font-semibold">
      <input v-model="feed.notes" placeholder="Notes" class="w-full border-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 h-10 px-3"></input>
    </div>
    <div>
      <SubmitButton :label="labelName" @click="addFeedData"></SubmitButton>
    </div>
  </div>
</template>