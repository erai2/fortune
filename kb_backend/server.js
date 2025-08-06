require('dotenv').config();
const express = require('express');
const cors = require('cors');
const fs = require('fs');
const fetch = require('node-fetch');
const app = express();
app.use(cors());
app.use(express.json());

const DATA_FILE = './data/terms.json';
if (!fs.existsSync('./data')) fs.mkdirSync('./data');

function loadTerms() {
  if (!fs.existsSync(DATA_FILE)) return [];
  return JSON.parse(fs.readFileSync(DATA_FILE, 'utf-8'));
}
function saveTerms(terms) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(terms, null, 2));
}

async function getAIJSON(prompt) {
  const res = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`
    },
    body: JSON.stringify({
      model: 'gpt-3.5-turbo',
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.3
    })
  });
  const data = await res.json();
  return JSON.parse(data.choices[0].message.content);
}

async function getEmbedding(text) {
  const res = await fetch('https://api.openai.com/v1/embeddings', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`
    },
    body: JSON.stringify({ input: text, model: 'text-embedding-ada-002' })
  });
  const data = await res.json();
  return data.data[0].embedding;
}

function cosineSim(a, b) {
  let s = 0, sa = 0, sb = 0;
  for (let i = 0; i < a.length; ++i) {
    s += a[i] * b[i];
    sa += a[i] ** 2;
    sb += b[i] ** 2;
  }
  return s / (Math.sqrt(sa) * Math.sqrt(sb));
}

app.post('/api/terms', async (req, res) => {
  const prompt = `\n아래 명리학 설명/용어를 category, term, definition, example JSON 구조로 정리해줘.\n설명: """${req.body.text}"""\n형식: {"category": "...", "term": "...", "definition": "...", "example": "..."}\n  `;
  const obj = await getAIJSON(prompt);
  obj.id = Date.now();
  obj.related_terms = req.body.related_terms || [];
  obj.embedding = await getEmbedding(obj.term + " " + obj.definition);
  const terms = loadTerms();
  terms.push(obj);
  saveTerms(terms);
  res.json(obj);
});

app.get('/api/terms', (req, res) => {
  res.json(loadTerms());
});

app.post('/api/terms/search', async (req, res) => {
  const query = req.body.query;
  const qemb = await getEmbedding(query);
  const terms = loadTerms();
  const sims = terms.map(t => ({ ...t, sim: cosineSim(qemb, t.embedding) }));
  sims.sort((a, b) => b.sim - a.sim);
  res.json(sims.slice(0, 10));
});

const PORT = 8000;
app.listen(PORT, () => console.log('Backend on http://localhost:' + PORT));

