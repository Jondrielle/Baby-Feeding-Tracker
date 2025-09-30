<script setup>
import { ref, watch,computed,onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useFeedingsStore } from '@/stores/feedings'
import { useUnitToggleStore } from '@/stores/unitToggle'
import DropDown from '@/components/DropDown.vue'
import FeedingForm from '@/components/FeedingForm.vue' 



const unitToggleStore = useUnitToggleStore()
const feedStore = useFeedingsStore()

const {
  filteredFeedings,
  filterType,
  filterValue
} = storeToRefs(feedStore)

const { deleteFeed,setFilter,fetchFeedings,clearFeeds,editFeed} = feedStore 

const filterMethod = ref('')
const editedFeed = ref(null)

const filterOptions = ['Clear', 'breastfeeding', 'bottle', 'food']

onMounted(async () => {
  await feedStore.fetchFeedings()
})

// When dropdown changes, update the filter
watch(filterMethod, (newVal) => {
  if (newVal === 'Clear' || newVal === '') {
    feedStore.setFilter('', '')  // clear filter
  } else {
    feedStore.setFilter('method', newVal)
  }
})

// Helper function to convert amount
const convertAmount = (amount, unit) => {
  const num = parseFloat(amount)
  if (isNaN(num)) return 'N/A'

  return unit === 'ml'
    ? (num * 29.5735).toFixed(0) // oz to ml
    : num.toFixed(1)             // keep oz
}

// Helper function to edit feed data
const editFeedData = (feed)=>{
  editedFeed.value = {...feed}
}

// Clear feed form
const closeForm = () => {
  editedFeed.value = null
}

// Save edited feed
const saveFeed = async (updatedFeed) => {
  await feedStore.editFeed(updatedFeed) // update store
  closeForm() // then close modal
}

const displayedFeedings = computed(() =>
  filteredFeedings.value.map(feed => {
    const amount = feed.amount_oz ?? feed.amount_ml ?? 0
    const displayAmount = convertAmount(
      amount,
      unitToggleStore.unitToggle === 'oz' ? 'oz' : 'ml'
    )
    return { ...feed, displayAmount }
  })
)

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
            <DropDown
              v-model="filterMethod"
              name="Filter"
              :options="filterOptions"
              iconType="filter"
              displayMode="filter"
              class="w-40"
              :isModal="false" 
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
        <tr v-for="feed in displayedFeedings" :key="feed.id" class="hover:bg-gray-50">
          <td class="px-4 py-2">{{ feed.method }}</td>
          <td class="px-4 py-2">{{ feed.displayAmount }}</td>
          <td class="px-4 py-2">{{ feed.time }}</td>
          <td class="px-4 py-2">{{ feed.notes }}</td>
          <td class="px-4 py-2">
            <button
              class="text-blue-600 hover:text-blue-700 active:scale-95 transition-transform"
              @click="editFeedData(feed)"
            >
              Edit 
            </button>
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
    <div class="mt-2 flex justify-start">
      <button class="text-red-600 hover:underline hover:text-red-700 active:scale-95 transition-transform" @click="clearFeeds()">Clear</button>
    </div>

    <!-- Modal -->
    <div v-if="editedFeed" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
      <div class="bg-white p-6 rounded-lg shadow-lg w-full max-w-lg">
        <FeedingForm :feed="editedFeed" @save="saveFeed" @cancel="closeForm"/>
      </div>
    </div>

  </div>
</template>
