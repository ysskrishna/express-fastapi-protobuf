<template>
  <div class="pagination" role="navigation" aria-label="pagination">
    <button
      @click="changePage(currentPage - 1)"
      :disabled="currentPage === 1 || disabled"
      class="pagination-button"
    >
      Previous
    </button>
    <span class="page-info">
      Page {{ currentPage }} of {{ totalPages }}
      <span class="total-count">({{ totalCount }} quotes)</span>
    </span>
    <button
      @click="changePage(currentPage + 1)"
      :disabled="currentPage === totalPages || disabled"
      class="pagination-button"
    >
      Next
    </button>
  </div>
</template>

<script>
export default {
  name: 'PaginationControls',
  props: {
    currentPage: { type: Number, required: true },
    totalPages: { type: Number, required: true },
    totalCount: { type: Number, required: true },
    disabled: { type: Boolean, default: false }
  },
  emits: ['page-change'],
  methods: {
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.$emit('page-change', page);
      }
    }
  }
};
</script>

<style scoped>
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 30px;
}
.pagination-button {
  padding: 10px 20px;
  border: 2px solid #667eea;
  background: white;
  color: #667eea;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
}
.pagination-button:hover:not(:disabled) {
  background: #667eea;
  color: white;
}
.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.page-info {
  font-size: 1.1rem;
  color: #333;
}
.total-count {
  color: #666;
  font-size: 0.9rem;
  margin-left: 5px;
}
</style>

