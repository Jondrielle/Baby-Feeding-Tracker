<script setup>
import { ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useFeedingsStore } from '@/stores/feedings'
import { useUnitToggleStore } from '@/stores/unitToggle'
import Dropdown from '@/components/Dropdown.vue'


const unitToggleStore = useUnitToggleStore()
const feedStore = useFeedingsStore()

const {
  filteredFeedings,
  filterType,
  filterValue
} = storeToRefs(feedStore)

const { deleteFeed, setFilter } = feedStore // ✅ FIX: include setFilter

const filterMethod = ref('')

const filterOptions = ['Clear', 'Breastfeeding', 'Bottle', 'Food']

// When dropdown changes, update the filter
watch(filterMethod, (newVal) => {
  if (newVal === 'Clear' || newVal === '') {
    feedStore.setFilter('', '')  // clear filter
  } else {
    feedStore.setFilter('method', newVal)
  }
})

// Optional: used for other filter buttons like amount/time
const filter = (type, value) => {
  setFilter(type, value)
}
</script>


<template>
  <div class="w-full overflow-x-auto">
    <table class="min-w-full border border-gray-200 rounded-lg divide-y divide-gray-200 min-h-[225px]">
      <thead class="bg-gray-100">
        <tr class="max">

          <!-- Method column header -->
          <th class="px-4 py-2 text-left text-gray-700 font-medium flex items-center space-x-2">
            <span>Method</span>
            <Dropdown
              v-model="filterMethod"
              name="Filter"
              :options="filterOptions"
              iconType="filter"
              displayMode="filter"
              class="w-40" 
            />
          </th>

          <!-- Amount column header -->
          <th class="px-4 py-2 text-left text-gray-700 font-medium">
            Amount ({{ unitToggleStore.unitToggle }})
            <button 
              @click="filter('amount')" 
              class="ml-2 p-1 text-gray-500 hover:text-gray-700" 
              aria-label="Filter by amount"
            >
              <span class="material-symbols-outlined">filter_alt</span>
            </button>
          </th>

          <!-- Time column header -->
          <th class="px-4 py-2 text-left text-gray-700 font-medium">
            Time
            <button 
              @click="filter('time')" 
              class="ml-2 p-1 text-gray-500 hover:text-gray-700" 
              aria-label="Filter by time"
            >
              <span class="material-symbols-outlined">filter_alt</span>
            </button>
          </th>
          
          <!-- Notes column header -->
          <th class="px-4 py-2 text-left text-gray-700 font-medium">Notes</th>
          
          <!-- Actions column header -->
          <th class="px-4 py-2 text-left text-gray-700 font-medium">Actions</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-100">
        <tr v-for="(feed, index) in filteredFeedings" :key="index" class="hover:bg-gray-50">
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
