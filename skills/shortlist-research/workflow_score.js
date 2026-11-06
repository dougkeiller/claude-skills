export const meta = {
  name: 'shortlist-score',
  description: 'Extract, dedupe, and rubric-score candidates from discovery docs into a ranked longlist (Fable only — no premium models)',
  phases: [
    { title: 'Extract', detail: 'Fable agents extract + prelim-score candidates from each discovery doc', model: 'fable' },
    { title: 'Rank', detail: 'dedupe across docs and rank to top N' },
  ],
}

// args: { docs: [{cell, text}], rubric: string, profile: string, topN: number }
// Tolerate args arriving as a JSON string OR an object.
let A = args
if (typeof A === 'string') { try { A = JSON.parse(A) } catch (e) { A = {} } }
A = A || {}
const docs = Array.isArray(A.docs) ? A.docs : []
const rubric = A.rubric || 'best overall fit for the stated goal'
const profile = A.profile || ''
const topN = A.topN || 24

if (!docs.length) {
  log('No discovery docs passed in args.docs — nothing to score.')
  return { total_unique: 0, longlist: [] }
}

const CANDIDATE_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    candidates: {
      type: 'array',
      maxItems: 40,
      items: {
        type: 'object',
        additionalProperties: false,
        properties: {
          name: { type: 'string' },
          cell: { type: 'string' },
          summary: { type: 'string' },          // <=40 words
          key_facts: { type: 'string' },         // cost / location / dates / eligibility, <=40 words
          score: { type: 'number' },             // 0-100 against the rubric
          score_rationale: { type: 'string' },   // <=30 words
        },
        required: ['name', 'summary', 'score'],
      },
    },
  },
  required: ['candidates'],
}

phase('Extract')
// Cost cap: never more than 8 extraction agents. Chunk docs round-robin if there are more.
const chunks = docs.length <= 8
  ? docs.map(d => [d])
  : (() => {
      const out = Array.from({ length: 8 }, () => [])
      docs.forEach((d, i) => out[i % 8].push(d))
      return out
    })()

const extracted = await parallel(chunks.map((chunk, i) => () =>
  agent(
    `You are extracting and scoring candidate options from web-research notes for this decision.\n\n` +
    `DECISION CONTEXT / PROFILE:\n${profile}\n\n` +
    `SCORING RUBRIC (score each option 0-100 against this; higher = better fit):\n${rubric}\n\n` +
    `From the research notes below, extract EVERY distinct real option. For each: name, the cell/segment it came from, a <=40-word summary, <=40 words of key facts (cost, location, dates, eligibility/age), a 0-100 score against the rubric, and a <=30-word rationale. ` +
    `Do NOT invent options or facts that are not in the notes. If the notes are thin on an option, score conservatively and say so.\n\nNOTES:\n\n` +
    chunk.map(d => d.text
      ? `## CELL: ${d.cell}\n${d.text}`
      : `## CELL: ${d.cell}\nRead the file at this absolute path with the Read tool and treat its FULL contents as the notes for this cell: ${d.path}`
    ).join('\n\n---\n\n'),
    { label: `extract:${i + 1}`, phase: 'Extract', model: 'fable', agentType: 'general-purpose', schema: CANDIDATE_SCHEMA }
  )
)).then(rs => rs.filter(Boolean).flatMap(r => (r.candidates || [])))

phase('Rank')
// Dedupe by normalized name, keep the highest-scored instance of each.
const byName = new Map()
for (const c of extracted) {
  if (!c || !c.name) continue
  const key = c.name.toLowerCase().replace(/\([^)]*\)/g, ' ').replace(/[^a-z0-9]+/g, ' ').trim()
  const prev = byName.get(key)
  if (!prev || (c.score || 0) > (prev.score || 0)) byName.set(key, c)
}
const ranked = Array.from(byName.values()).sort((a, b) => (b.score || 0) - (a.score || 0))
log(`Extracted ${extracted.length} rows -> ${ranked.length} unique candidates; returning top ${Math.min(topN, ranked.length)}.`)
return { total_unique: ranked.length, longlist: ranked.slice(0, topN) }
