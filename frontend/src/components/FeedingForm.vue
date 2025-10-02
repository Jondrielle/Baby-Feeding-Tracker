<script setup>
import { ref, watch } from 'vue'
import { useFeedingsStore } from '@/stores/feedings'
import { useUnitToggleStore } from '@/stores/unitToggle'
import SubmitButton from '@/components/SubmitButton.vue'
import DropDown from '@/components/DropDown.vue'

const unitToggleStore = useUnitToggleStore()
const feedStore = useFeedingsStore()
const { addFeed } = feedStore

const emit = defineEmits(['save', 'cancel'])

const props = defineProps({
  feed: Object // provided when editing
})

const isEditing = ref(!!props.feed)

const form = ref({
  id: null,
  method: '',
  amount_oz: '',
  amount_ml: '',
  time: '',
  notes: ''
})

watch(
  () => props.feed,
  (newFeed) => {
    if (newFeed) {
      isEditing.value = true
      // Only populate if form.id is null (first render)
      if (!form.value.id) {
        form.value = { ...newFeed }
      }
    } else {
      isEditing.value = false
      form.value = { id: null, method: '', amount_oz: '', amount_ml: '', time: '', notes: '' }
    }
  },
  { immediate: true }
)


const cancelForm = () => {
  emit('cancel')
}

const submitForm = () => {
  if (isEditing.value) {
    emit('save', form.value)  // parent closes modal
  } else {
    addFeed({
      method: form.value.method,
      amount_oz: unitToggleStore.unitToggle === 'oz' ? Number(form.value.amount_oz) : null,
      amount_ml: unitToggleStore.unitToggle === 'ml' ? Number(form.value.amount_oz) : null,
      time: form.value.time,
      notes: form.value.notes
    })
    form.value = { id: null, method: '', amount_oz: '', amount_ml: '', time: '', notes: '' }
  }
}


</script>

<template>
  <form @submit.prevent="submitForm">
    <div class="grid grid-cols-1 md:grid-cols-4 gap-3 py-3 px-4 bg-gray-50 rounded-lg shadow-sm w-full">
      
      <!-- Method -->
      <template v-if="isEditing">
        <div>
          <!-- Native select for edit modal -->
          <select v-model="form.method" required class="w-full border-2 border-gray-300 rounded-md h-10 px-3">
            <option value="" disabled>Select method</option>
            <option v-for="option in ['breastfeeding', 'bottle', 'food']" :key="option" :value="option">
              {{ option }}
            </option>
          </select>
        </div>
      </template>

        <template v-else>
          <!-- Dropdown for add form -->
          <DropDown 
            v-model="form.method"
            required
            name="Method"
            iconType="arrow"
            displayMode="form"
            class="w-full"
          />
        </template>
      <!-- Amount -->
      <input
        required
        v-model="form.amount_oz"
        type="number"
        :placeholder="'Amount (' + unitToggleStore.unitToggle + ')'"
        class="col-span-1 md:col-span-1 border-2 border-gray-300 rounded-md h-10 px-3 font-serif font-semibold w-full"
      />

      <!-- Time -->
      <input
        required
        v-model="form.time"
        type="datetime-local"
        class="col-span-1 md:col-span-1 border-2 border-gray-300 rounded-md h-10 px-3 font-serif font-semibold w-full"
      />

      <!-- Notes -->
      <input
        v-model="form.notes"
        placeholder="Notes"
        class="col-span-1 md:col-span-1 border-2 border-gray-300 rounded-md h-10 px-3 font-serif font-semibold w-full"
      />

      <!-- Buttons -->
      <div :class="['col-span-5 mt-2 flex gap-2', isEditing ? 'justify-end' : 'justify-center']">
        <SubmitButton
          type="submit"
          :label="isEditing ? 'Save' : 'Add'"
          class="border-2 border-gray-300 rounded-md h-10 px-4 font-semibold hover:bg-gray-100"
        />
        <button
          v-if="isEditing"
          type="button"
          @click="cancelForm"
          class="border-2 border-gray-300 rounded-md h-10 px-3 font-serif font-semibold text-gray-700 hover:bg-gray-100"
        >
          Cancel
        </button>
      </div>
    </div>

  </form>
</template>
