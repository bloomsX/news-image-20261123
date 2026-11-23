# news-image-20261123 — self-grade + build notes

## Entry
- `entry.png` — 1024×1024, 159,498 bytes, sha256 `06549cf8a39ecdd657ef555d2cfc443f9b82826fe284d20b1276309a35d5d70b`
- `draw.py` — v2 infographic style (3 big illustrated lead panels, 10 small drawn panels,
  big-number stats strip, numbered-pin world map, region bar, UTC timeline band,
  explicit DATE CHECK box, per-story source tags on every panel and every ALSO row).
- Research: `stories-23nov.md` (55 verified stories, marquee, excluded list, UTC timeline).
- Judge preview: `judge-preview/judge_ni23.py` + `judge-preview/results.jsonl`.

## Counts
- Stories: 55 (3 leads + 10 small + 42 ALSO)
- Regions: 7 geographic + Global — EUROPE 13 · ASIA 16 · OCEANIA 14 · MIDDLE EAST 4 ·
  N AMERICA 3 · LATAM 2 · AFRICA 1 · GLOBAL 2
- Fields: 12 (Politics, War, Climate, Markets, Tech, Sport, Culture, Disasters,
  Law, Health, Crime, Society)
- Marquee (5 most consequential, each with a named slot): 1 COP31 collapses (Antalya),
  2 Democrats take the House 258–177 (Washington), 3 Nikkei −5.06% AI sell-off (Tokyo),
  4 Merkury frigate sinks (Benghazi), 5 Russian strikes kill 12 in Kyiv region (Dymer).

## Self-grade (skill rubric, 0–100)
- Date gate: PASS. Every story verified as a 23 Nov 2026 event or first report.
  Two Tier-B items (ATEEZ Billboard No. 1, U2 album No. 4) were announced 22 Nov US
  but first reported 23 Nov Korea / on the 23 Nov chart — disclosed in research notes.
  Excluded items named in the DATE CHECK box (GTA 6 sales 20 Nov, Nvidia Q3 17 Nov,
  BYD EU ban 20 Nov, OpenRouter 22 Nov, Cairn zero-day 20 Nov, KPMG breach 18 Nov,
  RS-25 test 18 Nov).
- Breadth 35.9/40: stories 55/60 → 22.9/25; regions 7/7 → 10/10; fields 12/20 → 3.0/5.
  Ship floor is 35 — clears it, but only just (stories are the binding constraint:
  55 vs the 60-story reference).
- Marquee/selection 22/25: all 5 marquee slots are Tier-A, day-defining stories;
  the 5th slot (Dymer) could arguably be FIFA 2035 or the Taiwan short-selling ban,
  but 12 killed in Kyiv region is the stronger news call.
- Readability@300px 12/15: masthead, stats strip and all 3 lead headlines fully
  readable at 300px; small-panel headlines distinguishable; ALSO list and map labels
  not readable at 300px (same as ni22 v2). Floor is 12 — exactly at it.
- Faithfulness 9/10: every story carries a named source tag; no hype or speculation
  shown as fact; the two Tier-B items are the only softness.
- Craft 9/10: illustrated panels, map with numbered pins, stats strip, UTC timeline,
  region bar, DATE CHECK box; lead 2's detail sits 2px below its wrapped headline
  (tight but no overlap); map pins 3/8/9 cluster in East Asia (numbers still legible).
- TOTAL ≈ 88/100. Ship threshold: ≥80 total AND breadth ≥35 → SHIP.

## 300px legibility test
- Downscaled to 300×300 (`entry-300.png`): masthead, date, stats numbers and lead
  headlines readable; small-panel headlines fuzzy but distinguishable; ALSO unreadable
  at 300px. PASS at the same standard ni22 v2 passed at.

## Judge preview (free stand-in nvidia/nemotron-3.5-super-vl:free)
- Rivals: our own previous entries (ni23 dev board is blind, /tmp rivals gone):
  ni22 v2 ×4, ni21 r3 ×4, ni22 v1 ×2 — 10 games, A/B order alternated,
  kit's real judge instructions/rubric.
- Result: **9W / 1L** (10 games, A/B order alternated, free stand-in
  nvidia/nemotron-3.5-super-vl:free, kit's real judge instructions/rubric).
  vs ni22 v2: 3W/1L (margins 3, 2, 3, 3); vs ni21 r3: 4W/0L (margins 3, 4, 3, 3);
  vs ni22 v1: 2W/0L (margins 3, 3). The single loss (game 2, ours as B vs ni22 v2,
  margin 2) claimed our page reads as "overly concentrated on war and markets"
  vs the rival's broader fields — the reverse-order rematch (game 4) we won on
  breadth (12 fields vs 8), so the loss looks like cross-day noise, not a layout
  pattern. No layout/readability loss pattern like ni21's — NO rebuild needed.
  Recurring win reasons: breadth (55 stories / 12 fields vs rivals' 45 / 8),
  the UTC ticker, illustrated numbered panels + map legible at small sizes,
  and stats consistent with the stories. One judge note in our favour: it caught
  a stat/lead mismatch in ni22 v2 (Bahrain), not in ours.
  Caveat: rivals are cross-day own entries (ni23 dev board is blind), so this is
  a smoke test, not a dev rate — same limitation as the ni21/ni22 previews.
