import { getStore } from '@netlify/blobs';

// Key-value progress sync for the PIN-based accounts feature (T-10).
// Key = SHA-256("knm-audio:" + PIN), computed client-side so the raw PIN
// never leaves the device. Value = { updatedAt, data: {<localStorage keys>} }.
export default async (req) => {
  const url = new URL(req.url);
  const store = getStore('knm-progress');

  if (req.method === 'GET') {
    const key = url.searchParams.get('key');
    if (!key) return new Response('Missing key', { status: 400 });
    const payload = await store.get(key, { type: 'json' });
    if (payload === null) return new Response('Not found', { status: 404 });
    return new Response(JSON.stringify(payload), { headers: { 'Content-Type': 'application/json' } });
  }

  if (req.method === 'POST') {
    let body;
    try { body = await req.json(); } catch { return new Response('Invalid JSON', { status: 400 }); }
    const { key, payload } = body || {};
    if (!key || !payload) return new Response('Missing key/payload', { status: 400 });
    await store.setJSON(key, payload);
    return new Response(JSON.stringify({ ok: true }), { headers: { 'Content-Type': 'application/json' } });
  }

  return new Response('Method not allowed', { status: 405 });
};

export const config = { path: '/api/progress' };
