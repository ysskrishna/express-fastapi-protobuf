import { query, validationResult } from 'express-validator';
import express from 'express';

export function createQuotesRouter(protoTypes, service) {
  const router = express.Router();

  router.get(
    '/api/quotes',
    [
      query('tag').exists().withMessage('tag parameter is required').isString(),
      query('page').optional().isInt({ min: 1 }).toInt(),
      query('page_size').optional().isInt({ min: 1 }).toInt()
    ],
    async (req, res) => {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }
      try {
        const { tag, page = '1', page_size = '10' } = req.query;
        const json = await service.fetchQuotes(protoTypes, { tag, page, page_size });
        res.json(json);
      } catch (error) {
        console.error('Error fetching quotes:', error);
        res.status(500).json({ error: 'Failed to fetch quotes', details: error.message });
      }
    }
  );

  return router;
}

