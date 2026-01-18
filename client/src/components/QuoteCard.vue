<template>
  <div class="quote-card">
    <p class="quote-text">"{{ quote.text }}"</p>
    <p class="quote-author">— {{ quote.author }}</p>
    <div class="quote-tags">
      <span v-for="tag in quote.tags" :key="tag" class="quote-tag-badge">
        {{ tag }}
      </span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QuoteCard',
  props: {
    quote: {
      type: Object,
      required: true
    }
  }
};
</script>

<style scoped>
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
</style>

