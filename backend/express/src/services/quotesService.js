import axios from 'axios';
import { create, toBinary, fromBinary, toJson } from '@bufbuild/protobuf';
import { FASTAPI_URL } from '../config.js';
import {
  QuoteRequestSchema,
  QuoteResponseSchema,
  TagsRequestSchema,
  TagsResponseSchema
} from '../generated/proto/quote_pb.js';

export async function fetchQuotes(params) {
  const { tag, page = 1, page_size = 10 } = params;

  const requestMessage = create(QuoteRequestSchema, {
    tag: String(tag),
    page: parseInt(String(page), 10),
    pageSize: parseInt(String(page_size), 10)
  });
  const buffer = toBinary(QuoteRequestSchema, requestMessage);

  const response = await axios.post(`${FASTAPI_URL}/quotes`, buffer, {
    headers: { 'Content-Type': 'application/x-protobuf' },
    responseType: 'arraybuffer'
  });

  const responseBuffer = new Uint8Array(response.data);
  const quoteResponse = fromBinary(QuoteResponseSchema, responseBuffer);
  return toJson(QuoteResponseSchema, quoteResponse);
}

export async function fetchTags(params) {
  const { search = '', limit = 10 } = params;

  const requestMessage = create(TagsRequestSchema, {
    search: search || '',
    limit: parseInt(String(limit), 10)
  });
  const buffer = toBinary(TagsRequestSchema, requestMessage);

  const response = await axios.post(`${FASTAPI_URL}/tags`, buffer, {
    headers: { 'Content-Type': 'application/x-protobuf' },
    responseType: 'arraybuffer'
  });

  const responseBuffer = new Uint8Array(response.data);
  const tagsResponse = fromBinary(TagsResponseSchema, responseBuffer);
  return toJson(TagsResponseSchema, tagsResponse);
}
