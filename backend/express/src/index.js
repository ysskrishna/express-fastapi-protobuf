import express from 'express';
import { loadProto } from './lib/protoLoader.js';
import * as service from './services/quotesService.js';
import { createQuotesRouter } from './controllers/quotesController.js';
import { createTagsRouter } from './controllers/tagsController.js';
import cors from 'cors';
import { CORS_ORIGIN, PORT } from './config.js';

const app = express();
// Enable CORS for frontend
app.use(cors({
  origin: CORS_ORIGIN,
  methods: ['GET', 'POST', 'OPTIONS'],
  allowedHeaders: ['Content-Type'],
}));

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

