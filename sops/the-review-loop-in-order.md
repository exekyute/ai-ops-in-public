# Start Here: The Review Loop in Order (v1)

Seventeen review-side pieces now sit across six folders, plus three weekly maps in a seventh, at
versions from v1 to v4. The folders group by pillar, which is right for the repo and no help to a
person opening it for the first time, because nobody arrives needing "everything in `governance/`"
and nobody's job is "governance." This file orders the same pieces by when you need them: learn the
loop, do your part, keep and measure, see it run. Each entry gets one line on what it is for and when
to open it, and this index points rather than summarizes, because a summary competes with its source
and drifts from it, and an index that repeats content has to be rewritten every time any piece
changes. Pointing stays true longer than summarizing.

## Learn the loop

Read these once, in this order, before your first turn in any role below. They are the background
every role assumes.

1. `integration/week-02-review-and-handoff-loop.md`, The Review and Handoff Loop (v1). The shape of
   the loop, the five stages a finished build travels from done to shipped.
2. `standards/automation-standards.md`, Automation Standards (v2). The bar a build has to meet, the
   same bar the builder preps against and the reviewer grades against.
3. `governance/ai-build-review-checklist.md`, AI Build Review Checklist (v2). The gate, the
   line-by-line list that turns the bar into a decision.
4. `integration/week-03-the-loop-watching-itself.md`, The Loop Watching Itself (v1). Why the loop has
   to watch its own reviews, one ring further out.
5. `governance/review-spot-audit.md`, Review Spot-Audit (v1). The guardrail on the reviewer, a sample
   of decided builds re-reviewed by a third person.
6. `integration/week-04-the-loop-needs-people.md`, The Loop Needs People (v1). What it costs to run
   the loop with many builds and a pool of people.

## Do your part

Grouped by role. Read your row, skip the others until you take on that role.

**Builder, before every handoff**

- `enablement/builder-self-check.md`, Builder Self-Check Before Handoff (v1). The prep only you can
  do, run before you hand anything over.
- `sops/hand-off-a-build-for-review.md`, SOP: Hand Off a Build for Review (v1). What goes in the
  packet, and the path the decision takes back.

**Reviewer, every review**

- `sops/run-a-build-review.md`, SOP: Run a Build Review (v2). How to run the review so two people
  reach the same call.
- `governance/ai-build-review-checklist.md`, AI Build Review Checklist (v2). Keep it open while you
  run the SOP; the filled copy is your message back.
- `governance/inspection-required-checks.md`, Checks a Running Build Cannot Vouch For (v1). The lines
  a passing run cannot answer, and what to open for each.
- `enablement/reviewing-without-rubber-stamping.md`, Reviewing Without Rubber-Stamping (v1). Read this
  first if you have never reviewed here before.

**Whoever assigns reviews**

- `sops/run-the-review-queue.md`, SOP: Run the Review Queue (v2). How waiting builds get ordered and
  assigned to someone who is not the builder.

**Whoever keeps the review log**

- `sops/review-log-spec.md`, The Review Log (v3). What a row is and which fields it carries.
- `enablement/keeping-the-review-log.md`, Keeping the Review Log (v1). The write-time check to run
  before you write any row.
- `governance/what-counts-as-one-handoff.md`, What Counts as One Handoff (v1). The ruling behind that
  check, for a build you have logged before.

**Auditor**

- `governance/review-spot-audit.md`, Review Spot-Audit (v1). How to pull the sample and run the second
  cold review.
- `enablement/handling-a-review-miss.md`, Handling a Review Miss (v1). The conversation after a miss,
  so it lands as calibration.

## Keep and measure

Two records and the numbers read off them.

- `sops/review-log-spec.md`, The Review Log (v3). The permanent record, one row per handoff.
- `sops/run-the-review-queue.md`, SOP: Run the Review Queue (v2). The live record, one row per arrival
  still waiting.
- `analytics/metric-definitions.md`, Metric Definitions (v4). The numbers read off those two records,
  with what each one can and cannot see.

## See it run

Three worked runs on synthetic builds. Read one when a piece above reads as abstract.

- `examples/a-build-through-the-loop.md`, A Build Through the Loop (v1). A build the reviewer catches
  and sends back, all five stages in order.
- `examples/a-rubber-stamped-approval.md`, A Rubber-Stamped Approval (v1). A false approval the
  metrics cannot see, caught later by the spot-audit.
- `examples/a-populated-log-and-queue.md`, A Populated Log and Queue (v1). Both records filled in with
  rows, and the three review-side metrics computed off them.

## Deliberately not here

`enablement/tool-adoption-stages.md` is about adopting a tool in general, and
`integration/week-01-automation-lifecycle.md` maps the wider automation lifecycle, of which review is
one stage. Both are worth reading and neither is part of this loop, so they are left out on purpose.

## What this index cannot do

- **It goes stale in a way the pieces do not.** Every entry above carries its version inline, and
  those versions move. Files get added, paths get renamed, and a wrong pointer is worse than none,
  because an index is trusted. When anything here is added, renamed, or re-versioned, this file is the
  first thing to re-check.
- **It is a path and not a curriculum.** Reading everything in order teaches the shape of the loop.
  Being able to run a review comes from the role guides and the worked examples.
- **Reading order is not doing order.** "Learn the loop" is a sequence you go through once. "Do your
  part" is whichever row is yours today, and you will only ever run one or two of them.
- **It cannot make a team adopt any of this.** It makes the set enterable by someone who has never
  seen it. That is the whole claim.

---

*v1. A living index. Every added, renamed, or re-versioned review-side file gets fixed here in the
same pass, or this file starts lying about the folder it sits in.*
