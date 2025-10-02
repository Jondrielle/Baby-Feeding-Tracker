<script setup>
import { ref, watch,computed,onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useFeedingsStore } from '@/stores/feedings'
import { useUnitToggleStore } from '@/stores/unitToggle'
import DropDown from '@/components/DropDown.vue'
import FeedingForm from '@/components/FeedingForm.vue' 
import { ChevronUpIcon, ChevronDownIcon } from '@heroicons/vue/20/solid'




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
const sortBy = ref('')          // 'amount' or 'time'
const sortDirection = ref('asc') // 'asc' or 'desc'


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

const sortColumn = (column) => {
  if (sortBy.value === column) {
    // toggle ascending/descending
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortBy.value = column
    sortDirection.value = 'asc'
  }
}

  const sortedFeedings = computed(() => {
  let list = [...filteredFeedings.value]

  if (sortBy.value === 'amount') {
    list.sort((a, b) => {
      const aVal = a.amount_oz ?? a.amount_ml ?? 0
      const bVal = b.amount_oz ?? b.amount_ml ?? 0
      return sortDirection.value === 'asc' ? aVal - bVal : bVal - aVal
    })
  } else if (sortBy.value === 'time') {
    list.sort((a, b) => {
      const aTime = new Date(a.time).getTime()
      const bTime = new Date(b.time).getTime()
      return sortDirection.value === 'asc' ? aTime - bTime : bTime - aTime
    })
  }

  return list.map(feed => {
    const amount = feed.amount_oz ?? feed.amount_ml ?? 0
    const displayAmount = convertAmount(amount, unitToggleStore.unitToggle === 'oz' ? 'oz' : 'ml')
    return { ...feed, displayAmount }
  })
})

function onOverlayClick(event) {
  // Ignore clicks on dropdowns inside the modal
  if (!event.target.closest('.dropdown-ignore-overlay')) {
    closeForm()
  }
}

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

          <!-- Amount column -->
          <th class="px-4 py-2 text-left text-gray-700 font-medium">
            <button @click="sortColumn('amount')">
              Amount ({{ unitToggleStore.unitToggle }})
              <ChevronUpIcon v-if="sortBy === 'amount' && sortDirection === 'asc'" class="w-4 h-4 inline ml-1"/>
              <ChevronDownIcon v-else-if="sortBy === 'amount' && sortDirection === 'desc'" class="w-4 h-4 inline ml-1"/>
            </button>
          </th>

          <!-- Time column -->
          <th class="px-4 py-2 text-left text-gray-700 font-medium">
            <button @click="sortColumn('time')">
              Time
              <ChevronUpIcon v-if="sortBy === 'time' && sortDirection === 'asc'" class="w-4 h-4 inline ml-1"/>
              <ChevronDownIcon v-else-if="sortBy === 'time' && sortDirection === 'desc'" class="w-4 h-4 inline ml-1"/>
            </button>
          </th>


          
          <!-- Notes column header -->
          <th class="px-4 py-2 text-left text-gray-700 font-medium">Notes</th>
          
          <!-- Actions column header -->
          <th class="px-4 py-2 text-left text-gray-700 font-medium">Actions</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-100">
        <tr v-for="feed in sortedFeedings" :key="feed.id" class="hover:bg-gray-50">
          <td class="px-4 py-2">{{ feed.method }}</td>
          <td class="px-4 py-2">{{ feed.displayAmount }}</td>
          <td class="px-4 py-2">{{ feed.time }}</td>
          <td class="px-4 py-2">{{ feed.notes }}</td>
          <td class="px-4 py-2">
            <div class="flex gap-2">
            <button
              class="px-3 py-1 text-blue-600 border border-blue-600 rounded hover:bg-blue-50 active:scale-95 transition-transform duration-150 font-medium text-sm"
              @click="editFeedData(feed)"
            >
              Edit 
            </button>
            <button
              class="px-3 py-1 text-red-600 border border-red-600 rounded hover:bg-red-50 active:scale-95 transition-transform duration-150 font-medium text-sm"
              @click="deleteFeed(feed)"
            >
              Delete
            </button>
            </div>
          </td>
        </tr>

        <!-- Inline edit row -->
        <div
          v-if="editedFeed"
          class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
          @click="closeForm"
        >
          <div class="bg-white p-6 rounded-lg shadow-lg w-full max-w-lg" @click.stop>
            <FeedingForm :feed="editedFeed" :isEditing="true" @save="saveFeed" @cancel="closeForm"/>
          </div>
        </div>

      </tbody>
    </table>
    <div class="mt-2 flex justify-start">
      <button class="text-red-600 hover:underline hover:text-red-700 active:scale-95 transition-transform" @click="clearFeeds()">Clear</button>
    </div>

  </div>
</template>
