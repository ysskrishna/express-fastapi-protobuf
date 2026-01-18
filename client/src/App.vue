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
:root {
  --bg-1: #f6f8fb;
  --bg-2: #eef3f8;
  --surface: #ffffff;
  --primary: #0f172a; /* near-black for headings */
  --accent: #0ea5a4;  /* teal accent */
  --muted: #6b7280;
  --shadow: rgba(15, 23, 42, 0.06);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: radial-gradient(circle at 10% 10%, var(--bg-2), var(--bg-1));
  min-height: 100vh;
  padding: 28px;
  color: var(--primary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app {
  max-width: 1100px;
  margin: 0 auto;
}

header {
  text-align: center;
  color: var(--primary);
  margin-bottom: 32px;
}

header h1 {
  font-size: 2.1rem;
  margin-bottom: 6px;
  letter-spacing: -0.5px;
}

.subtitle {
  font-size: 1rem;
  color: var(--muted);
}

main {
  background: var(--surface);
  border-radius: 14px;
  padding: 28px;
  box-shadow: 0 12px 36px var(--shadow);
}

section {
  margin-bottom: 32px;
}

h2 {
  color: var(--primary);
  margin-bottom: 18px;
  font-size: 1.25rem;
}

/* Tags Section */
.tag-search-container {
  margin-bottom: 18px;
}

.tag-search-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e6e9ef;
  border-radius: 10px;
  font-size: 1rem;
  transition: box-shadow 0.18s ease, border-color 0.18s ease;
  background: linear-gradient(180deg, #fff, #fbfdff);
}

.tag-search-input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 4px 14px rgba(14,165,164,0.08);
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag-button {
  padding: 8px 18px;
  border: 1px solid rgba(14,165,164,0.18);
  background: rgba(14,165,164,0.04);
  color: var(--primary);
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.95rem;
  transition: transform 0.18s ease, background 0.18s ease, color 0.18s ease;
}

.tag-button:hover {
  background: var(--accent);
  color: white;
  transform: translateY(-2px);
}

.tag-button.active {
  background: var(--accent);
  color: white;
  font-weight: 600;
  border-color: transparent;
}

.tag-count {
  margin-left: 6px;
  opacity: 0.85;
}

/* Quotes Section styles moved to `QuoteGrid.vue` and `QuoteCard.vue` */

.no-tags {
  text-align: center;
  padding: 20px;
  color: var(--muted);
  font-size: 1rem;
}
</style>
