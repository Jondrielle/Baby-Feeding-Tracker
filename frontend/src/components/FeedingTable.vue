<script setup>
import {reactive} from 'vue'
import { storeToRefs } from 'pinia'
import {useFeedingsStore} from '@/stores/feedings'

const feedStore = useFeedingsStore()
const { feedings } = storeToRefs(feedStore)   // reactive state
const { deleteFeed } = feedStore              // action

</script>

<template>
  <div class="w-full overflow-x-auto">
    <table class="min-w-full border border-gray-200 rounded-lg divide-y divide-gray-200">
      <thead class="bg-gray-100">
        <tr>
          <th class="px-4 py-2 text-left text-gray-700 font-medium">Method</th>
          <th class="px-4 py-2 text-left text-gray-700 font-medium">Amount</th>
          <th class="px-4 py-2 text-left text-gray-700 font-medium">Time</th>
          <th class="px-4 py-2 text-left text-gray-700 font-medium">Notes</th>
          <th class="px-4 py-2 text-left text-gray-700 font-medium">Actions</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-100">
        <tr v-for="(feed, index) in feedings" :key="index" class="hover:bg-gray-50">
          <td class="px-4 py-2">{{ feed.method }}</td>
          <td class="px-4 py-2">{{ feed.amount }}</td>
          <td class="px-4 py-2">{{ feed.time }}</td>
          <td class="px-4 py-2">{{ feed.notes }}</td>
          <td class="px-4 py-2">
            <button
              class="text-red-600 hover:text-red-700 active:scale-95 transition-transform"
              @click="deleteFeed(feed)"
            >
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>


