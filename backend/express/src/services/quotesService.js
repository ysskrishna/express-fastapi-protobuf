import axios from 'axios';
import { FASTAPI_URL } from '../config.js';

export async function fetchQuotes({ QuoteRequest, QuoteResponse }, params) {
  const { tag, page = 1, page_size = 10 } = params;
  const requestMessage = QuoteRequest.create({
    tag: String(tag),
    page: parseInt(String(page), 10),
    page_size: parseInt(String(page_size), 10)
  });
  const buffer = QuoteRequest.encode(requestMessage).finish();

  const response = await axios.post(`${FASTAPI_URL}/quotes`, buffer, {
    headers: { 'Content-Type': 'application/x-protobuf' },
    responseType: 'arraybuffer'
  });

  const responseBuffer = Buffer.from(response.data);
  const quoteResponse = QuoteResponse.decode(responseBuffer);
  return QuoteResponse.toObject(quoteResponse, {
    longs: String,
    enums: String,
    bytes: String,
    defaults: true,
    arrays: true,
    objects: true,
    oneofs: true
  });
}

export async function fetchTags({ TagsRequest, TagsResponse }, params) {
  const { search = '', limit = 10 } = params;
  const requestMessage = TagsRequest.create({
    search: search || '',
    limit: parseInt(String(limit), 10)
  });
  const buffer = TagsRequest.encode(requestMessage).finish();

  const response = await axios.post(`${FASTAPI_URL}/tags`, buffer, {
    headers: { 'Content-Type': 'application/x-protobuf' },
    responseType: 'arraybuffer'
  });

  const responseBuffer = Buffer.from(response.data);
  const tagsResponse = TagsResponse.decode(responseBuffer);
  return TagsResponse.toObject(tagsResponse, {
    longs: String,
    enums: String,
    bytes: String,
    defaults: true,
    arrays: true,
    objects: true,
    oneofs: true
  });
}

