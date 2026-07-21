# SOP: Run the Review Queue (v2)

**Purpose:** order the builds waiting on review and assign each one to a reviewer who is not its builder,
so no build starves, no build reaches a reviewer who cannot review it honestly, and no single person
becomes the point the whole loop waits on. Ordering keeps builds moving; the size of the pool of
independent people decides whether what they move through is a real review at all.

**When to use this:** any time more than one build is in flight at once. One handoff on its own needs no
queue (`sops/hand-off-a-build-for-review.md`). The second build waiting while the first is still under
review is the moment you need one.

**Who runs it:** whoever assigns reviews. The queue is shared to pull from, a board or a sheet everyone can
see, not one person's inbox to clear. One person owns keeping it, the way section 8 of
`standards/automation-standards.md` gives every shared thing a named, accountable owner: they make sure
each waiting build gets ordered and assigned, and they do not have to be the person who reviews any given
build.

## What the queue is

The queue is the list of builds that have been handed off and are waiting on a review decision. A build
enters when its handoff packet is accepted (`sops/hand-off-a-build-for-review.md`), and it leaves the queue
when a reviewer lands on a decision and that decision is logged (`sops/review-log-spec.md`). The queue
tracks the review pass in flight right now. The review log carries the permanent record: one row per
handoff, written when the first review lands, with the first-review outcome frozen for the life of the
build.

These are two separate lists, and one build can sit on both. A build sent back on its first review gets its
log row at that moment, first-review outcome frozen as Send back, and leaves the queue. When it is fixed
and re-submitted, it re-enters the queue for a re-review, and that first-review log row stays exactly as
written (`sops/review-log-spec.md`). So during a re-review a build holds a frozen log row and a fresh queue
row at the same time. Read the queue as what is waiting now, and the log as what has already been decided
at least once.

Keep it light. One short row per waiting build is enough:

- The build name (synthetic, like every name in this repo).
- Who built it, so the assignment rule below has something to check against.
- Its arrival time, when this build entered the queue, so you can order by age and see the oldest. A
  re-submission carries its own arrival time, later than the one frozen on its log row
  (`governance/what-counts-as-one-handoff.md`).
- Whether it is in the priority lane (below).
- Who it is assigned to, once you assign it. Empty until then.

That is the whole record while a build waits. It shows only what is waiting and who has it. The checklist
and the log already carry the rest. When the review lands and the row moves off the queue, the log spec
takes over and carries the fuller record.

## Ordering: which build is next

The order answers one question: of the builds waiting, which does a free reviewer pick up next.

- **Oldest first by default.** Order by handoff time, oldest at the top. A reviewer coming free takes the
  top eligible build. Oldest-first is what keeps a build from starving while newer ones jump ahead of it.
- **One small priority lane.** A build that is production-bound or blocking other work can go in a priority
  lane that gets picked up before the default line. Keep the lane small. If most builds are priority, none
  are, and you are back to oldest-first with extra steps.
- **A re-submission goes to the back.** A build sent back (`sops/run-a-build-review.md`) that comes back is
  a fresh arrival, and not a fresh handoff: it re-enters at the back at its new arrival time and takes its
  turn like any other waiting build. It does not keep the place its first submission held. The review log
  keeps its original row, first-review outcome frozen (`sops/review-log-spec.md`); only its place in the
  queue is new. One handoff can have more than one arrival, and
  `governance/what-counts-as-one-handoff.md` defines both words and gives the test for telling a
  re-submission from a genuinely new handoff. This matches the loop: a send-back returns to the start,
  rebuilds its packet, and hands off again (`sops/hand-off-a-build-for-review.md`).
- **Watch the oldest-waiting age.** The age of the build that has waited longest is your one signal that
  the queue is under-served. If the oldest build keeps getting older week over week, the queue is taking in
  builds faster than it clears them, and no reordering fixes that. See "Keeping it from stalling."

## Assignment: who reviews it

Ordering decides which build is next. Assignment decides who reviews it. Three rules, two of them hard.

- **Hard rule: the reviewer is never the builder.** A build is never assigned to the person who built it.
  This is the independence the whole loop rests on. A builder reviewing their own build is running the
  self-check again under a review's name (`enablement/builder-self-check.md`): the builder grading their
  own prep, carrying none of the second-person look a review is for. The reviewer SOP is explicit that you
  do not need to have built the thing, and that is the point (`sops/run-a-build-review.md`). That is why
  the row records who built it, so the assignment can route around them.
- **Hard rule: pull from a pool, not one person.** Draw each build's reviewer from a group, not a single
  funnel. Two reasons. A single reviewer is the point everything waits on, and the queue's throughput
  collapses to whatever that one person clears. And a pool is what later lets a spot-audit
  (`governance/review-spot-audit.md`) hand a build to a third person who was neither the builder nor the
  reviewer. One reviewer plus one builder leaves no third person for the audit to use.
- **Soft rule: vary who reviews whom.** Where the pool allows, do not let the same reviewer always take the
  same builder's work. A fixed pairing drifts into shared blind spots: the two settle into what they both
  stop checking. Rotating who reviews whom is the same move the spot-audit makes with its auditor, for the
  same reason. This one bends when the pool is small. The hard rules do not.

## The single point

The bottleneck this SOP closes looks like throughput, one reviewer being slow. Underneath it is a people
constraint, and no ordering rule reaches it.

The loop needs three distinct people to run as designed:

- a **builder**, who makes the thing,
- a **reviewer**, who is not the builder, who gives it the second-person look,
- an **auditor**, who is neither, who spot-checks that the review was real
  (`governance/review-spot-audit.md`).

Count the people, not the reviews. The loop degrades a step at each drop:

- **Three or more:** the loop runs as written. A build can be reviewed by a non-builder and later audited
  by a third person who was neither.
- **Two:** you can still review. Every build has a builder and a reviewer who is not the builder. What you
  lose is the audit's independence, because the only person left to audit a review is the one who built the
  thing or the one who reviewed it, and both are the exact people the audit exists to check
  (`governance/review-spot-audit.md`). You have a real review and no real audit.
- **One:** there is no review. A build handed off to its own builder is the self-check wearing a review's
  name. The ordering rules still run, the board still fills and empties, and nothing on it is a review.

This is why the reviewer-queue bottleneck is really about independence, and not only throughput. A slow
queue can come from a pool that is large enough but busy, and ordering plus a work-in-progress cap help
with that. A queue that cannot be reviewed at all is a pool that is too small, and no ordering rule fixes
that. You cannot assign your way to a third person who is not there. A perfectly ordered queue with one
person in the pool is a tidy record of self-checks.

## Keeping it from stalling

- **Cap work in progress.** Hold each reviewer to one or two open reviews at a time, no more. A reviewer
  holding five half-done reviews finishes none of them, and finishing one review beats starting five. A
  reviewer at their cap takes no new build until one of theirs lands, so the next build waits or goes to
  someone under their cap.
- **A build past its target age is a pool-too-small signal.** When a build sits past the target age you
  set, the queue is taking in builds faster than the pool can clear them, and the fix is more reviewers or
  fewer builds in flight, not a reviewer working faster. A review rushed to drain a backlog is the rubber
  stamp the rest of this repo is built to prevent (`enablement/reviewing-without-rubber-stamping.md`,
  `governance/review-spot-audit.md`). Speeding the reviewer up to make the number look better trades away
  the one thing the loop is for. Read the oldest-waiting age from the ordering section, and when it climbs,
  add to the pool or slow the intake. Reordering a queue that is structurally under-served only changes
  which build waits longest.

## What this does not settle

Be honest about the edges.

- **It does not set your target age or your pool size.** Both depend on how many builds you take in and how
  fast independent reviewers can honestly clear them, which this SOP cannot know for you. It gives you the
  number to watch (the oldest-waiting age) and the rule for reading it (a climb means the pool is too
  small), and leaves the actual threshold to whoever keeps the queue.
- **It cannot conjure a third independent person.** If your pool is two, this SOP can route reviews around
  builders and still cannot give you an independent audit. If your pool is one, it cannot give you a
  review. No ordering rule fixes a pool that is too small, and this SOP is ordering rules. The pool is a
  staffing fact, and this SOP can only tell you when it is too small, not fill it.
- **The queue is still a manual board.** This defines the shape: what a waiting row holds, how rows are
  ordered, how they are assigned. Whether that shape lives on a whiteboard, a shared sheet, or a table is
  left open, the way the review log leaves its own form open (`sops/review-log-spec.md`). It is a shape
  waiting for real rows, and it earns its keep only when builds actually get ordered and assigned on it
  every time.

## What changed in v2

- A returning build is a fresh **arrival** here, and not a fresh handoff. The old wording used "handoff"
  for the queue's unit and for the log's, which are two different things, and writing real rows
  (`examples/a-populated-log-and-queue.md`) showed the two readings disagree.
  `governance/what-counts-as-one-handoff.md` settles it and this SOP points there.
- The waiting row's date is named as its arrival time, so a re-submission's queue row and the frozen date
  on its log row are no longer described by the same phrase.
- The ordering rule is unchanged. A re-submission still enters at the back and takes its turn.

---

*v2. A living SOP. The next pass sets a real target waiting age and a pool floor once a stretch of live
queue shows what this loop can honestly clear, and names the first re-submission that jumped its place so
the ordering rule catches it.*
