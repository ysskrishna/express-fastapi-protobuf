import { query, validationResult } from 'express-validator';
import express from 'express';

export function createTagsRouter(protoTypes, service) {
  const router = express.Router();

  router.get(
    '/api/tags',
    [
      query('search').optional().isString(),
      query('limit').optional().isInt({ min: 1 }).toInt()
    ],
    async (req, res) => {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }
      try {
        const { search = '', limit = '10' } = req.query;
        const json = await service.fetchTags(protoTypes, { search, limit });
        res.json(json);
      } catch (error) {
        console.error('Error fetching tags:', error);
        res.status(500).json({ error: 'Failed to fetch tags', details: error.message });
      }
    }
  );

  return router;
}

