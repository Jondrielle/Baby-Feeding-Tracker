<script setup>
import {reactive} from 'vue'

const tablefeeds = ref({
	method: '',
	amount: '',
	time: '',
	notes: ''
})

const addFeed = ()=>{
	
}

const deleteFeed = ()=>{
	
}

</script>

<template>
	<div>
		<table class="table-auto w-340">
  		<thead class="px-4 py-2 text-left">
		    <tr>
		      <th>Method</th>
		      <th>Amount</th>
		      <th>Time</th>
		      <th>Notes</th>
		      <th>Actions</th>
		    </tr>
		</thead>
		  <tbody class="px-4 py-2 text-left">
		    <tr v-for="(feeding, i) in feedings" :key="i">
		      <td>{{ feeding.method }}</td>
		      <td>{{ feeding.amount }}</td>
		      <td>{{ feeding.time }}</td>
		      <td>{{ feeding.notes }}</td>
		      <Button class="text-red-600 hover:text-red-700 active:scale-99">Delete</Button>
		    </tr>
		  </tbody>
		</table>
	</div>
</template>

