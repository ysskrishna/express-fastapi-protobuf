import express from 'express';
import axios from 'axios';
import protobuf from 'protobufjs';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = 3000;
const FASTAPI_URL = 'http://localhost:8000';

// Enable CORS for Vue frontend
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', 'http://localhost:5173');
  res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') {
    return res.sendStatus(200);
  }
  next();
});

app.use(express.json());

// Load protobuf schema
const protoPath = path.join(__dirname, '../common/proto/quote.proto');
let root = null;
let QuoteRequest = null;
let QuoteResponse = null;
let TagsRequest = null;
let TagsResponse = null;

async function loadProto() {
  try {
    root = await protobuf.load(protoPath);
    QuoteRequest = root.lookupType('QuoteRequest');
    QuoteResponse = root.lookupType('QuoteResponse');
    TagsRequest = root.lookupType('TagsRequest');
    TagsResponse = root.lookupType('TagsResponse');
    console.log('Protobuf schema loaded successfully');
  } catch (error) {
    console.error('Error loading protobuf schema:', error);
    process.exit(1);
  }
}

// GET /api/quotes?tag=inspirational&page=1&page_size=10
app.get('/api/quotes', async (req, res) => {
  try {
    const { tag, page = '1', page_size = '10' } = req.query;
    
    if (!tag) {
      return res.status(400).json({ error: 'tag parameter is required' });
    }
    
    // Create QuoteRequest protobuf message
    const requestMessage = QuoteRequest.create({
      tag: tag,
      page: parseInt(page, 10),
      page_size: parseInt(page_size, 10)
    });
    
    // Serialize to binary
    const buffer = QuoteRequest.encode(requestMessage).finish();
    
    // Send to FastAPI
    const response = await axios.post(
      `${FASTAPI_URL}/quotes`,
      buffer,
      {
        headers: { 'Content-Type': 'application/x-protobuf' },
        responseType: 'arraybuffer'
      }
    );
    
    // Deserialize protobuf response
    const responseBuffer = Buffer.from(response.data);
    const quoteResponse = QuoteResponse.decode(responseBuffer);
    
    // Convert to JSON
    const jsonResponse = QuoteResponse.toObject(quoteResponse, {
      longs: String,
      enums: String,
      bytes: String,
      defaults: true,
      arrays: true,
      objects: true,
      oneofs: true
    });
    
    res.json(jsonResponse);
  } catch (error) {
    console.error('Error fetching quotes:', error);
    res.status(500).json({ error: 'Failed to fetch quotes', details: error.message });
  }
});

// GET /api/tags?search=insp&limit=10
app.get('/api/tags', async (req, res) => {
  try {
    const { search = '', limit = '10' } = req.query;
    
    // Parse limit, default to 10 if invalid
    const limitValue = parseInt(limit, 10);
    const finalLimit = (limitValue > 0) ? limitValue : 10;
    
    // Create TagsRequest protobuf message with search and limit
    const requestMessage = TagsRequest.create({
      search: search || '',
      limit: finalLimit
    });
    
    // Serialize to binary
    const buffer = TagsRequest.encode(requestMessage).finish();
    
    // Send to FastAPI
    const response = await axios.post(
      `${FASTAPI_URL}/tags`,
      buffer,
      {
        headers: { 'Content-Type': 'application/x-protobuf' },
        responseType: 'arraybuffer'
      }
    );
    
    // Deserialize protobuf response
    const responseBuffer = Buffer.from(response.data);
    const tagsResponse = TagsResponse.decode(responseBuffer);
    
    // Convert to JSON
    const jsonResponse = TagsResponse.toObject(tagsResponse, {
      longs: String,
      enums: String,
      bytes: String,
      defaults: true,
      arrays: true,
      objects: true,
      oneofs: true
    });
    
    res.json(jsonResponse);
  } catch (error) {
    console.error('Error fetching tags:', error);
    res.status(500).json({ error: 'Failed to fetch tags', details: error.message });
  }
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

// Start server
async function start() {
  await loadProto();
  app.listen(PORT, () => {
    console.log(`Node.js BFF server running on http://localhost:${PORT}`);
  });
}

start().catch(console.error);
