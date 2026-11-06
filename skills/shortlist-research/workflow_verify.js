export const meta = {
  name: 'shortlist-verify',
  description: 'Web-grounded fact-check per finalist (Perplexity), one batched Opus adversarial pass, then a Fable-written cited report',
  phases: [
    { title: 'Verify', detail: 'web-grounded fact-check per finalist', model: 'fable' },
    { title: 'Skeptic', detail: 'one batched Opus adversarial pass over all finalists', model: 'opus' },
    { title: 'Synthesize', detail: 'Fable writes the final ranked report', model: 'fable' },
  ],
}

// args: { finalists: [{name, claims}], profile: string, rubric: string }
// Tolerate args arriving as a JSON string OR an object.
let A = args
if (typeof A === 'string') { try { A = JSON.parse(A) } catch (e) { A = {} } }
A = A || {}
const finalists = Array.isArray(A.finalists) ? A.finalists : []
const profile = A.profile || ''
const rubric = A.rubric || ''

if (!finalists.length) {
  log('No finalists passed in args.finalists — nothing to verify.')
  return { report: '', finalists: [] }
}

const VERIFY_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    name: { type: 'string' },
    confirmed: { type: 'string' },       // confirmed facts, <=60 words
    corrections: { type: 'string' },     // discrepancies vs the claims, <=60 words
    open_questions: { type: 'string' },  // must-confirm-in-writing, <=40 words
    sources: { type: 'array', maxItems: 5, items: { type: 'string' } },
  },
  required: ['name', 'confirmed'],
}

phase('Verify')
const verified = await parallel(finalists.map(f => () =>
  agent(
    `Fact-check this shortlisted option using web-grounded search. Use the perplexity_research tool (search for it via ToolSearch: "select:mcp__perplexity__perplexity_research"). \n\n` +
    `DECISION CONTEXT:\n${profile}\n\n` +
    `OPTION: ${f.name}\n` +
    `CLAIMS TO VERIFY:\n${f.claims || '(none supplied — establish the key facts yourself: what it is, cost, location, dates, eligibility/age, and whether it currently operates)'}\n\n` +
    `Return: confirmed facts (<=60 words), any corrections/discrepancies vs the claims (<=60 words), open questions to confirm in writing (<=40 words), and up to 5 source URLs. ` +
    `Report ONLY what the search actually returned — never invent facts or URLs. If you cannot verify something, say so in open_questions.`,
    { label: `verify:${f.name}`.slice(0, 60), phase: 'Verify', model: 'fable', agentType: 'general-purpose', schema: VERIFY_SCHEMA }
  ).then(v => (v ? { ...v, claims: f.claims } : null))
)).then(rs => rs.filter(Boolean))

phase('Skeptic')
// ONE batched Opus pass over ALL finalists — shares context + prompt caching vs. N separate agents.
const SKEPTIC_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    verdicts: {
      type: 'array',
      maxItems: 20,
      items: {
        type: 'object',
        additionalProperties: false,
        properties: {
          name: { type: 'string' },
          verdict: { type: 'string', enum: ['solid', 'conditional', 'disqualified'] },
          strongest_objection: { type: 'string' }, // <=40 words
        },
        required: ['name', 'verdict', 'strongest_objection'],
      },
    },
  },
  required: ['verdicts'],
}
const skeptic = await agent(
  `You are an adversarial skeptic. For EACH option below, state the single strongest reason it might be wrong, unsafe, ineligible, or a poor fit for THIS decision, then assign a verdict: ` +
  `"solid" (no material caveat), "conditional" (works but has a must-confirm caveat), or "disqualified" (a real blocker). Be harsh and specific; default to "conditional" when any real caveat exists. Reason silently; emit only the compact fields.\n\n` +
  `DECISION CONTEXT:\n${profile}\n\nRUBRIC:\n${rubric}\n\n` +
  `VERIFIED FINALISTS:\n${JSON.stringify(verified.map(v => ({ name: v.name, confirmed: v.confirmed, corrections: v.corrections, open_questions: v.open_questions })), null, 1)}`,
  { label: 'skeptic:opus', phase: 'Skeptic', model: 'opus', effort: 'high', schema: SKEPTIC_SCHEMA }
)
const verdictByName = new Map(((skeptic && skeptic.verdicts) || []).map(v => [v.name, v]))

phase('Synthesize')
const merged = verified.map(v => {
  const vd = verdictByName.get(v.name) || {}
  return { ...v, verdict: vd.verdict || 'conditional', objection: vd.strongest_objection || '' }
})
const report = await agent(
  `Write a tight, skimmable markdown decision report for this research.\n\n` +
  `DECISION CONTEXT:\n${profile}\n\n` +
  `Rank these verified finalists best-first. Respect the skeptic verdicts: never rank a "disqualified" option above a "solid" one; list disqualified options in a short section at the bottom. ` +
  `Include: a one-paragraph intro; a ranked summary table (Option | key facts | verdict | one-line why); then a short section per option (what it is, why it fits, the strongest objection, open questions to confirm in writing, sources). ` +
  `Use ONLY the data provided below — do not invent facts or URLs.\n\nDATA:\n${JSON.stringify(merged, null, 1)}`,
  { label: 'synthesize', phase: 'Synthesize', model: 'fable' }
)
return { report, finalists: merged }
