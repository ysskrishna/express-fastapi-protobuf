import protobuf from 'protobufjs';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const protoPath = path.join(__dirname, '..', '..', '..', 'common', 'proto', 'quote.proto');

let root = null;
let QuoteRequest = null;
let QuoteResponse = null;
let TagsRequest = null;
let TagsResponse = null;

export async function loadProto() {
  try {
    root = await protobuf.load(protoPath);
    QuoteRequest = root.lookupType('QuoteRequest');
    QuoteResponse = root.lookupType('QuoteResponse');
    TagsRequest = root.lookupType('TagsRequest');
    TagsResponse = root.lookupType('TagsResponse');
    console.log('Protobuf schema loaded successfully from', protoPath);
    return { QuoteRequest, QuoteResponse, TagsRequest, TagsResponse };
  } catch (error) {
    console.error('Error loading protobuf schema:', error);
    throw error;
  }
}

