<script setup>
import {reactive} from 'vue'
import { storeToRefs } from 'pinia'
import {useFeedingsStore} from '@/stores/feedings'

const feedStore = useFeedingsStore()
const { feedings } = storeToRefs(feedStore)   // reactive state
const { deleteFeed } = feedStore              // action

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
		    <tr v-for="(feed, index) in feedings" :key="index">
		      <td>{{feed.method}}</td>
		      <td>{{feed.amount}}</td>
		      <td>{{feed.time}}</td>
		      <td>{{feed.notes}}</td>
		      <Button class="text-red-600 hover:text-red-700 active:scale-99" @click="deleteFeed">Delete</Button>
		    </tr>
		  </tbody>
		</table>
	</div>
</template>

