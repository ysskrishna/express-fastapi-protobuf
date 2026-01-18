<template>
  <div class="app">
    <header>
      <h1>Quote Recommender</h1>
      <p class="subtitle">Discover inspiring quotes by tag</p>
    </header>

    <main>
      <!-- Tag Selector -->
      <TagSelector
        v-model="tagSearch"
        :tags="tags"
        :loading="loadingTags"
        :error="tagsError"
        :selected="selectedTag"
        @search="onTagSearch"
        @select="selectTag"
      />

      <!-- Quotes Display (moved to QuoteGrid component) -->
      <QuoteGrid v-if="selectedTag" :selectedTag="selectedTag" :pageSize="pageSize" />
    </main>
  </div>
</template>

<script>
import TagSelector from './components/TagSelector.vue';
import QuoteGrid from './components/QuoteGrid.vue';
import { getTags } from './composables/api';

export default {
  name: 'App',
  components: {
    TagSelector,
    QuoteGrid
  },
  data() {
    return {
      tags: [],
      loadingTags: false,
      tagsError: null,
      tagSearch: '',
      selectedTag: null,
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
        const params = { limit: 10 };
        if (this.tagSearch) params.search = this.tagSearch;
        const data = await getTags(params);
        this.tags = data.tags || data.items || [];
      } catch (error) {
        this.tagsError = `Failed to load tags: ${error.message || error}`;
        console.error('Error loading tags:', error);
      } finally {
        this.loadingTags = false;
      }
    },
    onTagSearch() {
      clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(() => {
        this.loadTags();
      }, 300);
    },
    selectTag(tagName) {
      this.selectedTag = tagName;
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

/* Quotes Section styles moved to `QuoteGrid.vue` and `QuoteCard.vue` */

.no-tags {
  text-align: center;
  padding: 20px;
  color: #666;
  font-size: 1rem;
}
</style>
