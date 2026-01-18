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
  background: var(--surface, #ffffff);
  padding: 20px;
  border-radius: 12px;
  transition: transform 0.18s ease, box-shadow 0.18s ease;
  box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
  position: relative;
  overflow: hidden;
}

.quote-card::before {
  content: '';
  position: absolute;
  left: 16px;
  top: 12px;
  height: 4px;
  width: 56px;
  background: linear-gradient(90deg, var(--accent, #0ea5a4), #2563eb);
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
}

.quote-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
}

.quote-text {
  font-size: 1.05rem;
  line-height: 1.6;
  color: var(--primary, #0f172a);
  margin-bottom: 14px;
  font-style: italic;
}

.quote-author {
  font-weight: 600;
  color: var(--accent, #0ea5a4);
  margin-bottom: 10px;
}

.quote-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}

.quote-tag-badge {
  background: #f1f5f9;
  color: #475569;
  padding: 6px 10px;
  border-radius: 12px;
  font-size: 0.85rem;
}
</style>

