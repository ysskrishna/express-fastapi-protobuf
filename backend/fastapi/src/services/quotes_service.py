from typing import List, Dict, Tuple

def filter_quotes_by_tag(all_quotes: List[Dict], tag: str) -> List[Dict]:
    """Return list of quote dicts that contain the tag (case-insensitive)."""
    if not tag:
        return []
    matching = []
    for idx, quote_item in enumerate(all_quotes):
        quote_tags = quote_item.get("tags", [])
        if tag.lower() in [t.lower() for t in quote_tags]:
            matching.append({
                "id": idx + 1,
                "text": quote_item.get("quote", ""),
                "author": quote_item.get("author", ""),
                "tags": quote_tags
            })
    return matching

def paginate_items(items: List[Dict], page: int, page_size: int) -> Tuple[List[Dict], int, int]:
    """Return (paginated_items, total_count, total_pages)."""
    total_count = len(items)
    total_pages = (total_count + page_size - 1) // page_size if total_count > 0 else 1
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    return items[start_idx:end_idx], total_count, total_pages

def compute_tag_counts(all_quotes: List[Dict]) -> Dict[str, int]:
    counts = {}
    for quote_item in all_quotes:
        for tag in quote_item.get("tags", []):
            tag_lower = tag.lower()
            counts[tag_lower] = counts.get(tag_lower, 0) + 1
    return counts

