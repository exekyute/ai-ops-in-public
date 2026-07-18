# The Loop Needs People (v1)

This week shipped five pieces: a second worked example, a sorted review checklist, a new-reviewer guide, a
review-queue SOP, and a new metric. On their own they read as five loose documents. Put in order, they take
the loop from the one build and one reviewer weeks 2 and 3 quietly assumed to a loop running with a pool of
people at a real pace: see what one person misses, name what a person has to open, grow the pool, route many
builds to it, and measure whether the pool keeps up. Every one of them turns on a person actually looking, or
on having enough independent people to look, and that is the week's one truth: the loop's binding constraint
is people, and process can make that constraint visible but cannot supply it. This file is that map, and it
continues last week's, where week 3 wrapped a loop around a single reviewer and week 4 asks what it costs to
run that loop with many builds and many people.

## The loop

Weeks 2 and 3 ran the loop with one build and one reviewer. Run it with many builds and many people and the
same five stages each turn on a person looking, or on having enough independent people to look, from the miss
one person cannot see to the number that says whether the pool keeps up.

1. **See what one person misses.** One synthetic build ran perfectly and was approved with a secret typed
   straight into a node's authorization header. The send-back rate scored the handoff a clean zero, blind to
   it by construction, and the flaw shipped, until a later spot-audit pulled the approved handoff, opened the
   node, and caught the false approval. The same eyeball slid past the same item twice, once on the builder's
   self-check and once on the review, because a valid token gives no sign of where it lives. That is the case
   a second and third person exist for: the miss the loop's numbers cannot see until someone opens the node.
   *Piece:* `examples/a-rubber-stamped-approval.md`.

2. **Name what a person must open.** That one miss becomes a reusable rule. Every checklist line is answered
   one of three ways: the happy path shows it, an adversarial run shows it, or only inspection shows it. The
   third set is the trap, because a passing run there gives false reassurance while answering a different
   question than the check asked. The piece names those inspection-required lines (secrets, key scope,
   retries, versioning, owner) and says what to open for each, so "it runs" never stands in for "I looked,"
   and Day 022's single skip becomes a class of checks anyone can spot.
   *Piece:* `governance/inspection-required-checks.md`.

3. **Grow the pool.** A pool of reviewers is people, and people have to be taught to look. This onboards a
   new reviewer with four habits: run it mean, open the thing on the inspection-required lines, decide from
   the marks, and write the reason. It reframes the spot-audit as a feature of the role rather than a trap,
   since a rubber stamp looks exactly like real prep from the outside and the audit is the only thing that
   tells the two apart. It is honest about its own ceiling: it can teach the habits, it cannot install the
   care. This is how the pool of people who can review grows, one reviewer at a time.
   *Piece:* `enablement/reviewing-without-rubber-stamping.md`.

4. **Route many builds to the pool.** With more than one build in flight, the waiting builds get ordered by
   handoff age and each is assigned to a reviewer who is not its builder, drawn from a pool rather than one
   funnel. The SOP's center is a floor: the loop needs three distinct people, a builder, a reviewer who is
   not the builder, and an auditor who is neither. Below three it degrades a step at a time (two gives a real
   review but no independent audit; one is a self-check wearing a review's name). The bottleneck is
   independence, a pool constraint, not only throughput, and no ordering rule reaches it.
   *Piece:* `sops/run-the-review-queue.md`.

5. **Measure whether the pool keeps up, and feed back.** Review latency is the median wait from handoff to
   first-review decision, read beside the oldest-waiting age. It is a pool-capacity signal: when it climbs,
   the queue is taking in builds faster than independent reviewers can honestly clear them, and the fix is
   more reviewers or fewer builds in flight, not a reviewer working faster. That pointer, add to the pool,
   sends you back to stage 3, and that return closes the cycle. Both this number and the review miss rate go
   blind at a pool of one, where the fastest median in the file sits on top of no real review at all.
   *Piece:* `analytics/metric-definitions.md`.

## The handoffs

Most of the value sits in the seams between the pieces, not in the pieces on their own.

- The **example** is what makes the **checks** necessary. Day 022 is one concrete miss: a secret marked
  passing off a working build, by the builder and again by the reviewer. The inspection-required checks
  generalize that one miss into a rule, every line where a passing run is no evidence at all. Without the
  example locating the trap on a real line, the checks are a rule with no proof it bites; with it, the rule
  has a worked case behind every category-3 line.
- The **checks** are what the **new-reviewer guide** teaches. The guide's second habit is exactly "open the
  thing on the lines a run cannot answer," and it points straight at the checks file for what to open: the
  auth field on the node, the scopes on the credential, the version history, the owner register. The checks
  name the lines; the guide installs the move in a person, so growing the pool means growing the number of
  people who carry that one move.
- The **guide** grows the pool the **queue** assigns from, and the queue is what the guide's independence
  needs. The guide teaches one reviewer to look; the queue's hard rules decide who gets which build and
  enforce the three-people floor the guide assumes without naming. They are the same staffing question read
  from opposite ends. A guide with nobody onboarded is a habit no one holds, and a queue with a pool of one
  is a board that orders self-checks.
- The **queue** and the **latency metric** read the same waiting. The queue watches the oldest-waiting age as
  its live under-served signal; the metric reads review latency, the lagging companion, the median over
  builds already decided. One reads the live queue, one reads the log, and both point at the same fact:
  whether the pool can clear what it takes in.
- The **latency metric** points back at the **guide**. A latency that climbs while the miss rate holds is a
  pool problem, and the only real fix is more independent people, which sends you back to onboarding. That
  pointer from the last stage to the third is the loop closing, the same shape as every prior map's closing
  metric: measure the thing, and let the measure send you back to an earlier stage.

## The loop in one line

See the miss one person cannot catch, name the lines a person has to open, teach a new person the habit of
opening them, route many builds to a pool where the builder, the reviewer, and the auditor are three
different people, and let the wait tell you when the pool is too small, which sends you back to teaching the
next person.

## Where this fits in the last three loops

Week 1's map, `integration/week-01-automation-lifecycle.md`, had "review it before it ships" as one stage of
the automation lifecycle. Week 2's map, `integration/week-02-review-and-handoff-loop.md`, opened that one
stage into its own full loop, from the bar a build must meet to the number that says whether it arrived
ready, and it watched the build. Week 3's map, `integration/week-03-the-loop-watching-itself.md`, wrapped a
second loop around week 2's review stage and watched the review, one ring further out. Both of those maps
quietly assumed the same two things: one build in flight, and one reviewer looking at it.

This week runs that stack of loops with many builds and many people, and the assumption breaks in the open.
The moment a second build waits while the first is under review, you need a queue; the moment you route
around the builder, you need a second person; the moment you want to know the review was real, you need a
third. Weeks 2 and 3 built the loop and then watched it; week 4 asks what it costs to run it at that scale,
and the answer is a staffing-and-independence constraint every piece this week runs into and none of them
removes. Say it plainly: the loop's ceiling is people, their number, their independence, and their care, and
process only makes that ceiling visible.

Be honest about what running with a pool buys. Every piece this week can make the people constraint visible
and priced, and not one can fill it. The inspection-required checks name the exact line a reviewer must open,
and cannot open it for them. The queue routes a build to a non-builder and flags when the pool is too small,
and cannot conjure a third independent person who is not there. The latency metric prices the wait and reads
the pool against the intake, and cannot review a single build. The three-people floor is the shape of the
whole limit: below three the loop degrades no matter how well the queue is ordered, and no file in this repo
can supply the third person. Process makes the constraint legible, so a rubber stamp is detectable and a thin
pool is measurable. It does not staff the pool.

## What is still missing

Each piece is a v1, with the metric now at v4, and this map is a v1 too. A real program would close gaps this
map still has. It is all still specs and synthetic: the review queue and the review log are shapes with
defined rows and no real ones in them, so review latency and the review miss rate are formulas with nothing
to compute, and the queue's oldest-waiting age has no live board to read. The loop has never run with a real
pool of real people: no queue anyone pulled from, no build assigned to a second person, no audit by a third.
The three roles are named, builder, reviewer, auditor, and the whole degrade-below-three argument rests on
filling all three, and none of them is filled here. The onboarding guide that grows the pool has onboarded
nobody, so the four habits are written and unpracticed, and the claim that they get faster with practice is a
claim, not a measurement.

The deepest gap is the one the pieces keep naming and none can close. Every file this week assumes people who
want to look: a reviewer willing to open a node on a build that already works, when nothing is forcing them
to. The queue can route a build to a second person and cannot make that person careful. The guide can teach
the habit and says outright it cannot install the care. The audit can catch a rubber stamp after the fact and
cannot make the next review real. Each of those can expose the missing care after the fact, and none can put
it there in the first place. The path is drawn for a pool. It has not been run by one, and the part that
matters most, people who care to look, is the part no document in here can write. Those are the threads the
coming weeks pull on.

---

*v1. A living map. The next pass runs the queue with a real pool of more than one person, so review latency
and the review miss rate have live rows behind them instead of a single synthetic build, and onboards a first
reviewer against the guide instead of describing one.*
