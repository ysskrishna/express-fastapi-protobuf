from fastapi import APIRouter, Request
from fastapi.responses import Response as FastAPIResponse
import sys
import os

# Ensure backend/fastapi is on path so `proto` package can be imported
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
try:
    from proto.quote_pb2 import QuoteRequest, QuoteResponse, Quote
except ImportError:
    raise

from ..repos.quotes_repo import get_all_quotes
from ..services.quotes_service import filter_quotes_by_tag, paginate_items

router = APIRouter()


@router.post("/quotes")
async def get_quotes(request: Request):
    body = await request.body()
    quote_request = QuoteRequest()
    quote_request.ParseFromString(body)

    tag = quote_request.tag
    page = quote_request.page if quote_request.page > 0 else 1
    page_size = quote_request.page_size if quote_request.page_size > 0 else 10

    all_quotes = get_all_quotes()
    matching = filter_quotes_by_tag(all_quotes, tag)
    paginated, total_count, total_pages = paginate_items(matching, page, page_size)

    response = QuoteResponse()
    response.tag = tag
    response.total_count = total_count
    response.page = page
    response.page_size = page_size
    response.total_pages = total_pages

    for q in paginated:
        quote_msg = Quote()
        quote_msg.id = q["id"]
        quote_msg.text = q["text"]
        quote_msg.author = q["author"]
        quote_msg.tags.extend(q["tags"])
        response.quotes.append(quote_msg)

    return FastAPIResponse(content=response.SerializeToString(), media_type="application/x-protobuf")

