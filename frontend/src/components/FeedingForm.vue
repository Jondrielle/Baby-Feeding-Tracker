<script setup>
import {ref, reactive,onMounted} from 'vue'
import { storeToRefs } from 'pinia'
import axios from 'axios';

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
const amount = ref('')
const formFeed = ref({
  method: '',
  amount_oz: null,
  amount_ml: null,
  time: '',
  notes: ''
})

const labelName = ref('Add')

const addFeedData = ()=>{

  formFeed.value.amount_oz = unitToggleStore.unitToggle === 'oz' ? Number(amount.value) : null

  formFeed.value.amount_ml = unitToggleStore.unitToggle === 'ml' ? Number(amount.value) : null

  // Add feed to store
  addFeed(formFeed.value)

  // Reset feed to empty values
  formFeed.value = {
    method: '',
    amount_oz: null,
    amount_ml: null,
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
            v-model="formFeed.method"
            required
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
            v-model="amount"
            type="number"
            :placeholder="'Amount (' + unitToggleStore.unitToggle + ')'"
            class="w-full border-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 h-10 px-3"
          />
        </div>

        <!-- Time -->
        <div class="font-serif font-semibold">
          <input
            required
            v-model="formFeed.time"
            type="datetime-local"
            placeholder="Time"
            class="w-full border-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 h-10 px-3 text-gray-500"
          />
        </div>

        <!-- Notes -->
        <div class="font-serif font-semibold">
          <input
            v-model="formFeed.notes"
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
