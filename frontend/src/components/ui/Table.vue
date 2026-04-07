<template>
  <div class="table-responsive rounded-4 border shadow-sm">
      <table class="table table-hover table-borderless align-middle mb-0 custom-table">
          <thead class="table-light border-bottom">
              <tr>
                  <th v-for="col in columns" :key="col.key" scope="col" 
                      :class="col.class || 'py-3 px-3 text-secondary fw-semibold text-uppercase'" 
                      style="font-size: 0.85rem; letter-spacing: 0.5px;">
                      {{ col.label }}
                  </th>
              </tr>
          </thead>
          <tbody>
              <tr v-for="(item, index) in data" :key="index" class="border-bottom">
                  <slot name="row" :item="item"></slot>
              </tr>
              <tr v-if="data.length === 0">
                  <slot name="empty">
                      <td :colspan="columns.length" class="text-center py-5 text-muted">
                          <div class="fs-1 mb-3 opacity-50">📋</div>
                          <h5 class="fw-bold">No data available</h5>
                      </td>
                  </slot>
              </tr>
          </tbody>
      </table>
  </div>
</template>

<script setup>
defineProps({
  columns: {
      type: Array,
      required: true
  },
  data: {
      type: Array,
      required: true
  }
})
</script>

<style scoped>
.custom-table tbody tr:last-child {
  border-bottom: 0 !important;
}
</style>
