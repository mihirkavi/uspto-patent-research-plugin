---
name: uspto-patent-research
description: Research U.S. patents and applications through the USPTO Open Data Portal, build prior-art landscapes and claim charts, inspect prosecution records, and develop patent disclosures or draft specifications. Use for USPTO searches, patentability research, novelty mapping, application metadata, continuity, transactions, document lists, claims planning, and patent-drafting support. Treat outputs as research rather than legal advice.
---

# USPTO Patent Research

Use the bundled `uspto_research` MCP tools to query the USPTO Open Data Portal (ODP). The server is read-only and forwards `USPTO_ODP_API_KEY` from the user's environment; never request or expose the key in chat, files, reports, commands, or tool arguments.

## Setup

1. When tools report that the API key is missing, read `references/setup.md` and guide the user through local credential setup.
2. Do not claim that installation proves live USPTO access; distinguish the offline protocol test from a credentialed API request.

## Research workflow

1. Define the invention as independently testable technical elements.
2. Search exact phrases, synonyms, likely CPC classes, inventors/assignees, and cited references.
3. Begin with title and metadata searching through ODP, then inspect individual applications, continuity, transactions, and document lists.
4. Supplement ODP with Patent Public Search, Google Patents, WIPO Patentscope, Espacenet, standards, papers, product documentation, and archived public disclosures. ODP metadata search alone is not a complete prior-art search.
5. Record publication numbers, priority dates, filing dates, status, assignee, relevant elements, and direct source links.
6. Build a claim-element matrix. Distinguish one-reference anticipation from multi-reference obviousness combinations.
7. Search backward and forward citations for the closest references.
8. Draft multiple claim families only after mapping the closest art.
9. Preserve alternatives, fallback positions, edge cases, and implementation detail sufficient to support later claims.

## Drafting boundaries

- Do not state that an invention is patentable, non-infringing, or clear of freedom-to-operate risk.
- Do not treat a provisional application as examined or granted.
- Distinguish patentability research from freedom-to-operate analysis.
- Identify missing inventor contributions, dates, public disclosures, and ownership facts.
- Recommend review by a registered U.S. patent practitioner before filing.
- Never submit a filing, pay fees, sign declarations, or represent the user before the USPTO.

## Resources

- Read `references/setup.md` only when installing, troubleshooting, or configuring the MCP server.
- Read `references/odp-api.md` when constructing ODP queries or interpreting responses.
- Read `references/patent-workflow.md` when producing a landscape, claim chart, disclosure, or application draft.

## Tool failure handling

- Treat HTTP 401 or 403 as a credential or USPTO account-state problem.
- Treat HTTP 429 as rate limiting; do not retry aggressively.
- If ODP is unavailable or incomplete, continue with other public sources and label which facts were not verified through ODP.
