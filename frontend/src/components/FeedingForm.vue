<script setup>
import {ref, reactive} from 'vue'

import SubmitButton from '@/components/SubmitButton.vue'
import DropDown from '@/components/DropDown.vue'

const required = true
const feeding = reactive({
  method: '',
  amount: '',
  time: '',
  notes: ''
})

const labelName = ref('Add')
const emit = defineEmits(['add-feeding']);

const setFeedData= ()=>{
  emit('add-feeding', { ...feeding})

  feeding.method = ''
  feeding.amount = ''
  feeding.time = ''
  feeding.notes = ''
}
</script>

<template>
  <div class="grid grid-cols-5 gap-2 py-3 px-4">
    <div class="font-serif font-semibold">
      <DropDown name="Method" :required="true" v-model="feeding.method" class="w-full"/>
    </div>
    <div class="font-serif font-semibold">
      <input v-model="feeding.amount" required type="number" placeholder="Amount" class="w-full border-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 h-10 px-3"></input>
    </div>
    <div class="font-serif font-semibold">
      <input v-model="feeding.time" required type="datetime-local" placeholder="Time" class="w-full border-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 px-3 text-[#8e8e8e] h-10"></input>
    </div>
    <div class="font-serif font-semibold">
      <input v-model="feeding.notes" placeholder="Notes" class="w-full border-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 h-10 px-3"></input>
    </div>
    <div>
      <SubmitButton :label="labelName" @click="setFeedData"></SubmitButton>
    </div>
  </div>
</template>