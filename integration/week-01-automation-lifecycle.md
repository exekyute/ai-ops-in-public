# The Automation Lifecycle (v1)

This week shipped five pieces: a standard, a review checklist, an SOP, an adoption model, and a
metric. On their own they read as five loose documents. Put in order, they are five stages of
one loop that a shared automation moves through, from the moment someone builds it to the moment
you know whether it is working. This file is that map.

## The loop

An automation that other people depend on goes through the same five stages every time.

1. **Build it to a standard.** Before anything else, the build meets a baseline: clear naming,
   real error paths, safe retries, no duplicate writes, scoped secrets, enough logging.
   *Piece:* `standards/automation-standards.md`.

2. **Review it before it ships.** Someone other than the builder checks it against that baseline
   and makes a call: approve, approve with fixes, or send back. The checklist is what they mark.
   The SOP is how they run the review so two people reach the same decision.
   *Pieces:* `governance/ai-build-review-checklist.md`, `sops/run-a-build-review.md`.

3. **Get people using it.** A reviewed, working automation that nobody reaches for is shelfware.
   People move through stages when they pick up a tool, and adoption is something you move one
   stage at a time rather than a switch you flip.
   *Piece:* `enablement/tool-adoption-stages.md`.

4. **Measure whether it works.** Once it is live and in use, you need a number behind "is this
   working," not a feeling. Exception rate is the first one: the share of runs that did not
   finish on their own.
   *Piece:* `analytics/metric-definitions.md`.

5. **Feed it back.** This stage is what makes it a loop instead of a line. What you measure in
   stage 4 tells you what to fix in stage 1 and what to tighten in stage 2.

## The handoffs

Most of the value sits in the seams between the pieces, not in the pieces on their own.

- The **standard** sets the bar the **review** checks against. Change the standard and the
  checklist has to follow, or the review starts passing builds the standard would fail.
- The **review** is the gate before **adoption**. Pushing people onto a build that has not
  passed review is how you teach them to distrust the tool.
- **Adoption** is what produces enough runs for the **metric** to mean anything. A rate measured
  on a tool nobody uses is noise.
- The **metric** is what sends you back to the **standard**. If exception rate climbs because
  one failure keeps recurring, that failure belongs in the standard as a new rule and in the
  checklist as a new line.

## The loop in one line

Build it right, prove it is right, get it used, measure whether it is working, and let what you
learn change how you build the next one.

## What is still missing

Each piece is a v1, and so is the loop. A real program would close gaps this map still has:
there is no rollback step for when a live build starts failing, no owner named for each stage,
and no cadence for how often the metric gets read and by whom. Those are the threads the coming
weeks pull on.

---

*v1. A living map. Each later pass adds a stage the real work turned up, or tightens a handoff
that leaked.*
