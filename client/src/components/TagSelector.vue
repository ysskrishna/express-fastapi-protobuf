<template>
  <section class="tags-section">
    <h2>Select a Tag</h2>
    <div class="tag-search-container">
      <input
        v-model="localSearch"
        @input="onInput"
        type="text"
        placeholder="Search tags... (showing top 10 by default)"
        class="tag-search-input"
        aria-label="Search tags"
      />
    </div>

    <div v-if="loading" class="loading">Loading tags...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="tags.length === 0" class="no-tags">No tags found matching your search.</div>

    <div v-else class="tags-container" role="list">
      <button
        v-for="tag in tags"
        :key="tag.name"
        @click="$emit('select', tag.name)"
        :class="['tag-button', { active: selected === tag.name }]"
        role="listitem"
      >
        {{ tag.name }}
        <span class="tag-count">({{ tag.count }})</span>
      </button>
    </div>
  </section>
</template>

<script>
export default {
  name: 'TagSelector',
  props: {
    tags: { type: Array, default: () => [] },
    loading: { type: Boolean, default: false },
    error: { type: String, default: null },
    modelValue: { type: String, default: '' },
    selected: { type: String, default: null }
  },
  emits: ['update:modelValue', 'select'],
  data() {
    return {
      localSearch: this.modelValue
    };
  },
  watch: {
    modelValue(newVal) {
      this.localSearch = newVal;
    }
  },
  methods: {
    onInput() {
      this.$emit('update:modelValue', this.localSearch);
      this.$emit('search', this.localSearch);
    }
  }
};
</script>

<style scoped>
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
</style>

