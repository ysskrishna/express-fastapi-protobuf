from fastapi import APIRouter, Request
from fastapi.responses import Response as FastAPIResponse
import sys
import os

# Ensure backend/fastapi is on path so `proto` package can be imported
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
try:
    from proto.quote_pb2 import TagsRequest, TagsResponse, TagInfo
except ImportError:
    raise

from ..repos.quotes_repo import get_all_quotes
from ..services.quotes_service import compute_tag_counts

router = APIRouter()


@router.post("/tags")
async def get_tags(request: Request):
    body = await request.body()
    tags_request = TagsRequest()
    tags_request.ParseFromString(body)

    search_query = tags_request.search.lower() if tags_request.search else ""
    limit = tags_request.limit if tags_request.limit > 0 else 0

    tag_counts = compute_tag_counts(get_all_quotes())

    if search_query:
        tag_counts = {name: cnt for name, cnt in tag_counts.items() if search_query in name}

    sorted_tags = sorted(tag_counts.items(), key=lambda x: (-x[1], x[0]))
    if limit > 0:
        sorted_tags = sorted_tags[:limit]

    response = TagsResponse()
    response.total_tags = len(tag_counts)
    for tag_name, count in sorted_tags:
        tag_info = TagInfo()
        tag_info.name = tag_name
        tag_info.count = count
        response.tags.append(tag_info)

    return FastAPIResponse(content=response.SerializeToString(), media_type="application/x-protobuf")

