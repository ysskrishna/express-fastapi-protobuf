import express from 'express';
import { loadProto } from './lib/protoLoader.js';
import * as service from './services/quotesService.js';
import { createQuotesRouter } from './controllers/quotesController.js';
import { createTagsRouter } from './controllers/tagsController.js';

const app = express();
const PORT = 3000;

// Enable CORS for frontend
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

async function start() {
  const protoTypes = await loadProto();
  app.use(createQuotesRouter(protoTypes, service));
  app.use(createTagsRouter(protoTypes, service));

  app.get('/health', (req, res) => res.json({ status: 'ok' }));

  app.listen(PORT, () => {
    console.log(`Express BFF running on http://localhost:${PORT}`);
  });
}

start().catch((err) => {
  console.error('Failed to start express server:', err);
  process.exit(1);
});

