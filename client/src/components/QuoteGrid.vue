<template>
  <section class="quotes-section" v-if="selectedTag">
    <h2>Quotes: {{ selectedTag }}</h2>

    <div v-if="loading" class="loading">Loading quotes...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="quotes.length === 0" class="no-quotes">No quotes found for this tag.</div>

    <div v-else>
      <div class="quotes-grid">
        <QuoteCard
          v-for="quote in quotes"
          :key="quote.id || quote._id || quote.uid"
          :quote="quote"
        />
      </div>

      <PaginationControls
        :currentPage="currentPage"
        :totalPages="totalPages"
        :totalCount="totalCount"
        :disabled="loading"
        @page-change="goToPage"
      />
    </div>
  </section>
</template>

<script>
import QuoteCard from './QuoteCard.vue';
import PaginationControls from './PaginationControls.vue';
import { getQuotes } from '../composables/api';

export default {
  name: 'QuoteGrid',
  components: { QuoteCard, PaginationControls },
  props: {
    selectedTag: { type: String, required: true },
    pageSize: { type: Number, default: 10 }
  },
  data() {
    return {
      quotes: [],
      loading: false,
      error: null,
      currentPage: 1,
      totalCount: 0,
      totalPages: 1
    };
  },
  watch: {
    selectedTag(newTag, oldTag) {
      if (newTag !== oldTag) {
        this.currentPage = 1;
        this.loadQuotes();
      }
    }
  },
  mounted() {
    if (this.selectedTag) this.loadQuotes();
  },
  methods: {
    async loadQuotes() {
      if (!this.selectedTag) return;
      this.loading = true;
      this.error = null;
      try {
        const params = {
          tag: this.selectedTag,
          page: this.currentPage,
          page_size: this.pageSize
        };
        const data = await getQuotes(params);
        this.quotes = data.quotes || data.items || data.results || [];
        this.totalCount = data.total_count || data.total || data.totalCount || 0;
        this.totalPages = data.total_pages || data.totalPages || Math.max(1, Math.ceil(this.totalCount / this.pageSize));
        this.currentPage = data.page || data.current_page || data.page_number || this.currentPage;
      } catch (err) {
        this.error = `Failed to load quotes: ${err.message || err}`;
        console.error('Error loading quotes:', err);
      } finally {
        this.loading = false;
      }
    },
    goToPage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
        this.loadQuotes();
      }
    }
  }
};
</script>

<style scoped>
.quotes-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
  margin-bottom: 30px;
}
.no-quotes {
  text-align: center;
  padding: 40px;
  color: #666;
  font-size: 1.1rem;
}
</style>

