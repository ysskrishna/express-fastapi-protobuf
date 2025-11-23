<template>
  <div class="app">
    <header>
      <h1>Quote Recommender</h1>
      <p class="subtitle">Discover inspiring quotes by tag</p>
    </header>

    <main>
      <!-- Tag Selector -->
      <section class="tags-section">
        <h2>Select a Tag</h2>
        <div class="tag-search-container">
          <input
            v-model="tagSearch"
            @input="onTagSearch"
            type="text"
            placeholder="Search tags... (showing top 10 by default)"
            class="tag-search-input"
          />
        </div>
        <div v-if="loadingTags" class="loading">Loading tags...</div>
        <div v-else-if="tagsError" class="error">{{ tagsError }}</div>
        <div v-else-if="tags.length === 0" class="no-tags">
          No tags found matching your search.
        </div>
        <div v-else class="tags-container">
          <button
            v-for="tag in tags"
            :key="tag.name"
            @click="selectTag(tag.name)"
            :class="['tag-button', { active: selectedTag === tag.name }]"
          >
            {{ tag.name }}
            <span class="tag-count">({{ tag.count }})</span>
          </button>
        </div>
      </section>

      <!-- Quotes Display -->
      <section v-if="selectedTag" class="quotes-section">
        <h2>Quotes: {{ selectedTag }}</h2>
        
        <div v-if="loadingQuotes" class="loading">Loading quotes...</div>
        <div v-else-if="quotesError" class="error">{{ quotesError }}</div>
        <div v-else-if="quotes.length === 0" class="no-quotes">
          No quotes found for this tag.
        </div>
        <div v-else>
          <!-- Quote Cards -->
          <div class="quotes-grid">
            <div v-for="quote in quotes" :key="quote.id" class="quote-card">
              <p class="quote-text">"{{ quote.text }}"</p>
              <p class="quote-author">— {{ quote.author }}</p>
              <div class="quote-tags">
                <span
                  v-for="tag in quote.tags"
                  :key="tag"
                  class="quote-tag-badge"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>

          <!-- Pagination Controls -->
          <div class="pagination">
            <button
              @click="goToPage(currentPage - 1)"
              :disabled="currentPage === 1 || loadingQuotes"
              class="pagination-button"
            >
              Previous
            </button>
            <span class="page-info">
              Page {{ currentPage }} of {{ totalPages }}
              <span class="total-count">({{ totalCount }} quotes)</span>
            </span>
            <button
              @click="goToPage(currentPage + 1)"
              :disabled="currentPage === totalPages || loadingQuotes"
              class="pagination-button"
            >
              Next
            </button>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import axios from 'axios';

const API_BASE = 'http://localhost:3000/api';

export default {
  name: 'App',
  data() {
    return {
      tags: [],
      loadingTags: false,
      tagsError: null,
      tagSearch: '',
      selectedTag: null,
      quotes: [],
      loadingQuotes: false,
      quotesError: null,
      currentPage: 1,
      pageSize: 10,
      totalCount: 0,
      totalPages: 0
    };
  },
  mounted() {
    this.loadTags();
  },
  methods: {
    async loadTags() {
      this.loadingTags = true;
      this.tagsError = null;
      try {
        const params = {
          limit: 10  // Always limit to top 10
        };
        if (this.tagSearch) {
          params.search = this.tagSearch;
        }
        const response = await axios.get(`${API_BASE}/tags`, { params });
        this.tags = response.data.tags || [];
      } catch (error) {
        this.tagsError = `Failed to load tags: ${error.message}`;
        console.error('Error loading tags:', error);
      } finally {
        this.loadingTags = false;
      }
    },
    onTagSearch() {
      // Debounce search - reload tags after user stops typing
      clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(() => {
        this.loadTags();
      }, 300);
    },
    selectTag(tagName) {
      this.selectedTag = tagName;
      this.currentPage = 1;
      this.loadQuotes();
    },
    async loadQuotes() {
      if (!this.selectedTag) return;
      
      this.loadingQuotes = true;
      this.quotesError = null;
      try {
        const response = await axios.get(`${API_BASE}/quotes`, {
          params: {
            tag: this.selectedTag,
            page: this.currentPage,
            page_size: this.pageSize
          }
        });
        
        this.quotes = response.data.quotes || [];
        this.totalCount = response.data.total_count || 0;
        this.totalPages = response.data.total_pages || 1;
        this.currentPage = response.data.page || 1;
      } catch (error) {
        this.quotesError = `Failed to load quotes: ${error.message}`;
        console.error('Error loading quotes:', error);
      } finally {
        this.loadingQuotes = false;
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

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  padding: 20px;
}

.app {
  max-width: 1200px;
  margin: 0 auto;
}

header {
  text-align: center;
  color: white;
  margin-bottom: 40px;
}

header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
}

main {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

section {
  margin-bottom: 40px;
}

h2 {
  color: #333;
  margin-bottom: 20px;
  font-size: 1.5rem;
}

/* Tags Section */
.tag-search-container {
  margin-bottom: 20px;
}

.tag-search-input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.tag-search-input:focus {
  outline: none;
  border-color: #667eea;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag-button {
  padding: 10px 20px;
  border: 2px solid #667eea;
  background: white;
  color: #667eea;
  border-radius: 25px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.tag-button:hover {
  background: #667eea;
  color: white;
  transform: translateY(-2px);
}

.tag-button.active {
  background: #667eea;
  color: white;
  font-weight: bold;
}

.tag-count {
  margin-left: 5px;
  opacity: 0.8;
}

/* Quotes Section */
.quotes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.quote-card {
  background: #f8f9fa;
  border-left: 4px solid #667eea;
  padding: 20px;
  border-radius: 8px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.quote-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.quote-text {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #333;
  margin-bottom: 15px;
  font-style: italic;
}

.quote-author {
  font-weight: bold;
  color: #667eea;
  margin-bottom: 10px;
}

.quote-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-top: 10px;
}

.quote-tag-badge {
  background: #e9ecef;
  color: #495057;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.85rem;
}

/* Pagination */
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

/* Loading and Error States */
.loading {
  text-align: center;
  padding: 20px;
  color: #667eea;
  font-size: 1.1rem;
}

.error {
  text-align: center;
  padding: 20px;
  background: #fee;
  color: #c33;
  border-radius: 8px;
  border: 1px solid #fcc;
}

.no-quotes {
  text-align: center;
  padding: 40px;
  color: #666;
  font-size: 1.1rem;
}

.no-tags {
  text-align: center;
  padding: 20px;
  color: #666;
  font-size: 1rem;
}
</style>
