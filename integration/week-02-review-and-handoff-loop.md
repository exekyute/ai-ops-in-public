# The Review and Handoff Loop (v1)

This week shipped five pieces: a deepened standard, a builder self-check, a handoff SOP, a review
checklist with its reviewer SOP, and a new metric. On their own they read as five loose documents.
Put in order, they are the stages of one loop that a finished build travels to become a shipped,
approved build: the bar it must meet, the prep against that bar, the path it takes to the reviewer,
the gate the reviewer runs, and the number that says whether builds are arriving ready. This file is
that map. It also opens up one stage of last week's map: what week 1 called "review it before it
ships" is the whole loop below.

## The loop

A finished build moves through the same five stages every time on its way from done to shipped.

1. **Set the bar.** Before any of this runs, there is a baseline a build must meet, and it is the
   same baseline for the builder and the reviewer. This week the standard grew section 8 (Ownership)
   and section 9 (Change and rollback), so "an owner is named" and "there is a safe rollback" are now
   part of the bar, not afterthoughts.
   *Piece:* `standards/automation-standards.md`.

2. **Prep against the bar.** The builder does the work only they can do before handoff: run the happy
   path and a failure case, name one owner, set up a rollback, write the one-paragraph "what this does
   and why." This is the builder's side of the reviewer's checklist, so a clean self-check is a build
   already at the bar.
   *Piece:* `enablement/builder-self-check.md`.

3. **Hand it off.** The build crosses one named handoff point from builder to reviewer, carrying a
   handoff packet: the runnable build, the description, and confirmation the self-check is clean with an
   owner and a rollback in place. A partial packet is not a handoff, and a send-back returns along the
   same path it went out.
   *Piece:* `sops/hand-off-a-build-for-review.md`.

4. **Run the gate and decide.** Someone other than the builder runs the build against a good and a bad
   input, walks the checklist top to bottom, and lands on exactly one of three outcomes: Approve,
   Approve with fixes, or Send back. The checklist is what they mark; the reviewer SOP is how they run
   it so two people reach the same call.
   *Pieces:* `governance/ai-build-review-checklist.md`, `sops/run-a-build-review.md`.

5. **Measure and feed back.** This stage is what makes it a loop instead of a line. The send-back rate
   is the share of handoffs a reviewer sends back on the first review, and it says whether builds are
   arriving review-ready. When it climbs, the fix is a sharper self-check, not a stricter review. The
   number points back to stage 2.
   *Piece:* `analytics/metric-definitions.md`.

## The handoffs

Most of the value sits in the seams between the pieces, not in the pieces on their own.

- The **standard** is the one bar, and three pieces are three views of it. The self-check is the
  builder's view, the checklist is the reviewer's view, and the handoff SOP is the path between the
  two. When the standard added ownership and rollback, all three views added the matching lines the
  same week, or the builder would prep for one bar and the reviewer would grade against another.
- The **self-check** is what makes the **packet** assemblable. It is what produces the description, the
  named owner, the rollback, and the two runs, so a builder cannot hand off a complete packet without
  having done it. Skip the prep and the handoff has nothing to carry.
- The **packet** is what lets the **review** start at all. A reviewer who opens a packet with no
  runnable build or no description sends it straight back, because the reviewer SOP cannot begin without
  both. The packet is the whole message in, the filled checklist is the whole message back.
- The **review outcome** is what the **metric** counts. Send-back rate reads the review records, not
  the run logs: one row per handoff, the first-review outcome, a date. If reviews are decided verbally
  and no checklist is filled, the number has nothing to count.
- The **metric** is what sends you back to the **self-check**. A high send-back rate is a prep problem,
  not a review problem, so the number closes the loop by pointing at stage 2, not stage 4.

## The loop in one line

Set the bar, prep the build to it, hand it off clean, run the gate and decide, and let how often builds
bounce tell you where the prep needs to get sharper.

## Where this fits in last week's loop

Last week's map, `integration/week-01-automation-lifecycle.md`, had five stages, and stage 2 was "review
it before it ships": someone other than the builder checks the build and makes a call. This week is that
one stage opened into its own full loop. Week 1 named a stage; week 2 is what happens inside it, from the
bar the build must meet to the number that says whether it arrived ready. This loop-over-loop is the
point: week 1 named the gaps, week 2 closed them and went deeper on one segment.

That zoom-in also closes the three gaps week 1's map named as still missing:

- Week 1: "no owner named for each stage." Closed by standard v2 section 8 (Ownership), now a checklist
  item the reviewer marks and a self-check item the builder prepares. A named owner is part of the bar,
  the prep, and the gate.
- Week 1: "no rollback step for when a live build starts failing." Closed by standard v2 section 9
  (Change and rollback), now part of the self-check's prep and a required line in the handoff packet, so
  a build cannot pass without a versioned definition and a safe stop.
- Week 1: "no cadence for how often the metric gets read and by whom." Addressed by the checklist's
  ownership section, which asks that the health metric gets looked at on a set cadence with someone named
  to do it, and by each metric's own "how often to read it" line.

## What is still missing

Each piece is a v1 or v2, and so is this loop. A real program would close gaps this map still has. The
whole loop assumes an honest reviewer, and nothing here measures whether the review itself is real: a
reviewer who waves everything through drives the send-back rate to zero and the number stops meaning
anything. There is no worked example yet of a build going all the way around the loop, only the
questions each stage asks. The ownership and rollback rules are written but not backed by real registers
or templates, so "name an owner" still relies on a habit rather than a form. And this loop covers one
build at a time; it says nothing about a queue of builds waiting on one reviewer, which is where the next
bottleneck usually shows up. Those are threads the coming weeks pull on.

---

*v1. A living map. Each later pass adds a stage the real work turned up, or tightens a handoff that
leaked.*
