<script setup>
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue'
import { ChevronDownIcon } from '@heroicons/vue/20/solid'

const emit = defineEmits(['update:modelValue']);

const options = ['Breastfeeding','Bottle','Food']
const props = defineProps({
	name: String,
	modelValue: String,
	required:{
		type: Boolean,
	    default: false
	}	
})

const selectOption = (option) => {
  emit('update:modelValue', option) // notify parent
}
</script>

<template>
  <Menu as="div" class="relative inline-block w-55">
    <MenuButton class="inline-flex w-full justify-between items-center rounded-md border-2 border-gray-300 px-4 py-2 font-semibold text-[#8e8e8e] hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-green-500 h-10 w-56 ">
  {{ modelValue || name }}  <!-- show selected value or fallback to name -->
  <ChevronDownIcon class="w-5 h-5 ml-2" aria-hidden="true" />
</MenuButton>
	    <transition
	  enter-active-class="transition ease-out duration-100"
	  enter-from-class="transform opacity-0 scale-95"
	  enter-to-class="transform scale-100"
	  leave-active-class="transition ease-in duration-75"
	  leave-from-class="transform scale-100"
	  leave-to-class="transform opacity-0 scale-95"
	>
	  <MenuItems class="absolute z-10 mt-2 w-full origin-top-right rounded-md bg-gray-800 shadow-lg text-[#8e8e8e]">
	    <div class="py-1">
	      <MenuItem v-for="option in options" :key="option" v-slot="{ active }">
	        <button
	          @click="selectOption(option)"
	          :class="[active ? 'bg-gray-700 text-white' : 'text-gray-300', 'block w-full text-left px-4 py-2 text-sm']"
	        >
	          {{ option }}
	        </button>
	      </MenuItem>
	    </div>
	  </MenuItems>
	</transition>
  </Menu>
</template>