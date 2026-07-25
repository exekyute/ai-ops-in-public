# The Loop Gets Kept (v1)

This week shipped five pieces: a filled-in record, a counting ruling, a write-time guide for whoever holds
the pen, an index over the whole review side, and a memo on how that index gets checked. On their own they
read as five loose documents. Put in order, they are what upkeep turned out to consist of: fill the records
the specs described, settle what filling them exposed, put the ruling where a person meets it, make the
grown set findable, and decide how it gets checked. Nothing here was designed. Weeks 2, 3, and 4 built the
review loop, each day adding a piece somebody decided it still needed, and this week every day was a
consequence of work already written down. That is the week's one truth: upkeep is work the system hands you
rather than work picked off a roadmap, and a system that generates its own next task has started being
kept. This file is that map, and it continues last week's, where week 4 asked what the loop costs to run
with a pool of people.

## The loop

Weeks 2 to 4 moved through five stages chosen in advance. Keeping what those weeks wrote moves through five
stages too, and this week each one arrived as the problem the stage before it produced.

1. **Fill the record.** Day 029 turned two empty shapes into rows: twelve handoffs, a four-build queue
   snapshot read on Jul 20, and the three review-side metrics computed off them, a send-back rate of 3 in
   12, a latency median of 3.5 days beside an oldest-waiting age of 19, and a miss rate of 1 in 5 whose one
   overturn is a false approval. Read one at a time, two of the three look healthy; read as a set, the queue
   is not, since no number sees both the 19-day undecided build and the bad approval inside the passing
   column. Filling the log also forced `sops/review-log-spec.md` to v2 with a new required field, Handed
   off, because a wait cannot be computed from four columns carrying one date. Use is what tests a spec.
   *Piece:* `examples/a-populated-log-and-queue.md`.

2. **Settle what the use exposed.** Writing the rows put two records in open conflict. The queue SOP called
   a re-submission a fresh handoff and the log spec kept one row per handoff with the first-review outcome
   frozen, both right about the record they govern, because one word was doing two jobs. The ruling splits
   it: a handoff is one build's trip through review, an arrival is each entry into the queue, and one
   handoff can have many arrivals. The test is what the submission answers, so a submission answering an
   open send-back is the same handoff and anything else is new. It won on counting integrity, since a second
   row would let a bounced build dilute its own send-back rate. Queue SOP to v2, log spec to v3. A conflict
   found is a decision owed.
   *Piece:* `governance/what-counts-as-one-handoff.md`.

3. **Put the decision where a person meets it.** A ruling does not write rows. This is the write-time habit
   for whoever keeps the log: four steps before any row, nearly all of which stop at the first, since a
   build never logged before can only get a new row. The risk is all in the returning build, and the guide's
   center is its fail-safe. When you cannot tell whether a returning build is the same handoff, merge rather
   than split, because a wrongly-merged row is a quiet undercount by one while a wrongly-split row is the
   exact gaming the ruling exists to stop.
   *Piece:* `enablement/keeping-the-review-log.md`.

4. **Make the grown set findable.** The guide had just spread one person's job across three folders:
   whoever keeps the log needs the log spec, the guide, and the ruling held in relation, and a set organized
   by pillar cannot show a person which three files are theirs. Seventeen review-side pieces across six
   folders is past browsing besides. The index reorders the same pieces by when you need them (learn the
   loop, do your part, keep and measure, see it run), with the middle grouped by role so each reader reads
   one row and skips the rest. It names its own failure mode: it goes stale silently, and a wrong pointer
   is worse than none, because an index is trusted.
   *Piece:* `sops/the-review-loop-in-order.md`.

5. **Decide how the upkeep gets checked, and feed back.** The index's staleness claim looks like a request
   for a fifth metric. What it wants is a check. Every claim the index makes is settled against a tree still
   sitting there: a path resolves or it does not, a version claim matches an H1 or it does not. Staleness
   here is decidable, and estimating it costs the same exhaustive read while returning a percentage in place
   of the two file names that failed. Measure what you must estimate, test what you can decide. The check
   runs at the moment of the change that would break it, and change happens inside stages 1 to 4, so this
   stage points back at all of them at once.
   *Piece:* `analytics/measure-or-test.md`.

## The handoffs

Most of the value sits in the seams between the pieces, not in the pieces on their own.

- The **rows** are what made the **ruling** necessary. Every cross-check since `sops/run-the-review-queue.md`
  shipped on Day 025 had both records in hand, and four weeks of pieces citing each other by path and
  version had never produced a find like this. Twelve authored rows produced it in an afternoon, at the
  moment rows 1 and 4 had to be written differently three rows apart: the same build coming back with new
  work gets its own row, and the same build coming back after a send-back does not.
- The **ruling** is what the **guide** installs, and each names the other's limit. The ruling says outright
  that it settles the counting question and forces nobody to record it correctly. The guide answers that
  sentence by putting the question in front of the person before the row is written, the one moment it is
  cheap. The ruling gives two people the same answer; the guide is what makes them ask.
- The **guide** is one row inside the **index**, which is what the volume buys. The log spec, the guide, and
  the ruling sit under a single role heading, so whoever keeps the log reads three files and leaves the
  other fourteen alone.
- The **index** is what the **memo** checks, and it wrote the memo's requirements without meaning to. The
  memo reads the index's own limits paragraph as a specification: 22 distinct paths, 24 version claims, plus
  a rule the index never asked for, that every in-scope file appears at all. That third rule earns its keep,
  since the first two walk only the claims the index already makes, so a file it has never heard of passes
  both while the index goes quietly incomplete.
- The **memo** closes the ring differently from every prior week. Weeks 2, 3, and 4 each ended in a number
  pointing back at one earlier stage: the send-back rate at the prep, the miss rate at the review, latency
  at the pool. This one ends in a check whose trigger is the act of changing anything, and whose timing rule
  is the guide's rule generalized from a log row to a pointer. The feedback runs through editing rather than
  through measuring, which is what a maintenance loop looks like.

## The loop in one line

Fill the record and let the filling test the spec, settle the conflict the rows exposed, put the ruling in
front of whoever holds the pen, order the grown set so a newcomer can enter it, and decide how the set gets
checked at the moment somebody changes it, which puts you back inside every stage above.

## Where this fits in the last four loops

Week 1's map, `integration/week-01-automation-lifecycle.md`, mapped the wider automation lifecycle, of which
review is one stage, and Day 032's index leaves it out of this loop on purpose. The three after it are the
review loop's own: `integration/week-02-review-and-handoff-loop.md` opened week 1's "review it before it
ships" into a full loop, `integration/week-03-the-loop-watching-itself.md` wrapped a second loop around the
review, and `integration/week-04-the-loop-needs-people.md` ran that stack with a pool of people. Three
straight weeks of building, and in all three each day's artifact was a piece somebody decided the loop still
needed: a checklist because the review needed a gate, a queue because builds pile up behind one person.

Week 5 added nothing to that design. Day 029 filled the records week 4 had closed by calling empty shapes,
named the night before in Day 028's reflect as the week's first build, and that act exposed a conflict. Day
030 settled it. Day 031 put the ruling where a person would meet it. Day 032 indexed a set that had grown
past browsing. Day 033 decided how the index gets checked. Four of the five answered a problem the day
before created; the fifth, Day 032, answered three weeks of accumulated volume, which the day before had
only sharpened. Be exact about the bound: the pillar slot for each day was fixed in advance the way it is
every week, Build, Govern, Enable, Document, Analyze, in that order. What was not fixed was the subject that
filled it, and in weeks 2 to 4 that subject was a piece somebody chose, while in week 5 it was whatever the
day before had broken. Say it plainly: maintenance work is generated by the system rather than chosen from a
roadmap. A repo that hands you your next task has stopped being a pile of documents and started being a
thing that is kept.

The sharper point is where those tasks came from. Every problem this week found was found by use, and none
by review. The handoff conflict existed from the day the queue SOP shipped on Day 025, four days before Day
029, and in that window it passed one weekly map and the reflect after it without a careful reading turning
it up. Twelve rows surfaced it in an afternoon. A spec is only tested by being used, and the cheapest use is
filling it in with invented data. That cuts the other way too. The rows were written by the same person who
wrote the specs, so the use was sympathetic, and most of the awkward cases in Day 029's log are ones the
specs had already anticipated. A real user would find more.

## What is still missing

Each piece is a v1, with the log spec now at v3 and the queue SOP at v2, and this map is a v1 too. A real
program would close gaps this map still has. The records are authored, twelve log rows and four waiting
builds written by one person to exercise definitions that same person wrote, so Day 029 shows that the
metrics compute and nothing about a real queue. The ruling has met exactly one case, and the write-time
guide has been run against no rows at all.

The check is a specification, and this repo has shipped no code. It was run once by hand on the day the
index shipped, 22 paths and 24 version claims, zero mismatches, which is a datapoint and not a habit. A
specified check nobody runs catches exactly as much as no check, the same shape as the log nobody keeps. And
the loop still has not run with real people: no queue anyone pulled from, no build assigned to a second
person, no audit by a third.

The maps now have the problem they keep describing. Five weekly maps sit in `integration/`, and nothing
indexes them. Day 032's index lists three of them as background and has no idea this file exists, so this
map is the second unindexed file in the tree, after the memo that named the rule which would flag it. That
rule has never been run: the one hand pass predates it and read paths and versions only. Those are the
threads the coming weeks pull on.

---

*v1. A living map. The next pass runs the check instead of describing it, indexes the maps themselves, and
reports what the next week generated on its own, since a week nobody planned is evidence of a kept system
only if it happens twice.*
