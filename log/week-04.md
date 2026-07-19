# Week 4 Log

Days 022 to 027. Week 1 was breadth, week 2 was depth, and week 3 turned the loop on itself with an audit.
This week's job was scale: take the loop from the one build and one reviewer weeks 2 and 3 quietly assumed,
and run it with a pool of people at a real pace. Ship a second worked example, sort the checklist by what a
person has to open, onboard a new reviewer, document the queue that routes many builds to many people, define
the metric that says whether the pool keeps up, and map the five as one loop. Six days, six artifacts, one
loop scaled to a pool, and one thing it cannot scale past: people.

## What shipped

- `examples/a-rubber-stamped-approval.md`: v1, a second worked example, the false-approval counterpart to
  week 3's honest send-back, a build approved with a secret typed into a node that the send-back rate scored
  a clean zero and the spot-audit caught only by opening the node.
- `governance/inspection-required-checks.md`: v1, the checklist lines a running build cannot vouch for,
  sorted by what answers each one (the happy path, an adversarial run, or inspection only), with exactly what
  to open for every inspection-only line.
- `enablement/reviewing-without-rubber-stamping.md`: v1, the new-reviewer guide, four habits that separate a
  real review from a rubber stamp, the spot-audit reframed as a feature, honest that it can teach the habits
  and cannot install the care.
- `sops/run-the-review-queue.md`: v1, the review queue with its ordering and assignment rules, its center a
  three-people floor: a builder, a reviewer who is not the builder, and an auditor who is neither. The
  bottleneck is independence, a pool constraint, not only throughput.
- `analytics/metric-definitions.md`: to v4, review latency, the median wait from handoff to first-review
  decision read beside the oldest-waiting age, carrying a survivorship trap (a stalled queue posts a fast
  median) and a blind spot at a pool of one.
- `integration/week-04-the-loop-needs-people.md`: v1, the five pieces mapped as one loop that scales to a
  pool, its title the finding.

## What I actually learned

I went into the week thinking the open problem was throughput: builds arrive faster than one reviewer clears
them, so order the queue better and push them through. That is not what the week was about. The bottleneck I
kept calling "one reviewer is slow" turned out to be a staffing fact, and no ordering rule reaches it. Every
piece I shipped could make the people constraint visible and put a price on it. The inspection-required
checks name the exact line a reviewer has to open. The queue flags when the pool is too thin. Review latency
prices the wait. Not one of them could fill the constraint: open the node for someone, conjure a third
independent person, or make anyone care to look. That gap is the ceiling. You can build all the machinery and
it still needs a person who wants to look, and no document in the repo supplies that.

The second thing the week taught is that independence is not free, and it fails the same way at two different
scales. Day 022 was the small scale: a build approved with a secret typed into a node, marked passing by the
builder and again by the reviewer, because both eyeballed the same item the same way. Two controls collapsed
into one look taken twice. A second check only helps if the second checker does the thing the first one
skipped. Day 025 was the same truth at the level of staffing. The loop needs three distinct people, a
builder, a reviewer who is not the builder, and an auditor who is neither, and below three it degrades
quietly: two gives a real review and no independent audit, one gives a self-check wearing a review's name.
The board still fills and empties either way, so a pool of one looks like it is working. Redundancy on paper
is a single point of failure in practice unless the second look is genuinely a different one, whether the
redundancy is two checks or two people.

The sharpest single day was the fourth metric, and the lesson was about where a number stops seeing. Every
metric in the file lies in the direction of its blind spot, and each one lies differently. Exception rate
cannot see the run that never fired, send-back rate cannot see the approval that should have bounced, and
review latency, the number I added this week, cannot see the build that is still waiting, because a median
over finished reviews counts only the builds that finished. That is the worst shape a queue number can take:
the more the queue rots, the better the median looks, since the builds sitting at the bottom never enter the
count. The blind spot sits exactly where the data stops, and no cleverer formula closes it. The cure is a
second number that reads a different record, the median off the log and the oldest-waiting age off the live
queue, read together. The finding that pulled the week together is that latency and the review miss rate go
blind at the same place. A pool of one posts the fastest median in the file, because a builder reviewing
their own build clears instantly and no audit exists to catch it, and both numbers stop seeing at exactly the
pool size where adding reviewers is the answer. Count the people before you read either one.

## What was thinner than I wanted

It is all still specs and synthetic, same as the last three weeks. The review queue and the review log are
shapes with defined rows and no real ones in them, so review latency and the review miss rate are formulas
with nothing to compute, and the oldest-waiting age has no live board to read. The second worked example is
one build with one planted secret, a single miss and not a pattern, caught only because the sample happened
to pull it. The loop has never run with a real pool: no queue anyone pulled from, no build handed to a second
person, no audit by a third. The three roles are named and none is filled, and the whole degrade-below-three
argument rests on filling all three. The onboarding guide that grows the pool has onboarded nobody, so its
four habits are written and unpracticed.

The deepest gap is the one every piece kept naming and none could close. Every file this week assumes a
person who wants to look, a reviewer willing to open a node on a build that already works when nothing is
forcing them. The queue can route a build to a second person and cannot make that person careful. The guide
can teach the habit and says outright it cannot install the care. The audit can catch a rubber stamp after
the fact and cannot make the next review real. Each of those exposes the missing care once it is already
missing, and none puts it there in the first place. The part that matters most, people who care to look, is
the part no document in here can write.

## Carrying into week 5

- Run the loop once with a real, populated pool, so the queue, the log, and their metrics finally have live
  rows behind them instead of a single synthetic build.
- Onboard or trace a first reviewer against the new-reviewer guide, so the four habits get practiced instead
  of only written.
- Keep closing the named gaps: the handoff-time field the log needs for latency, a real audit against filled
  rows, and the outer-edge auditor no control here reaches.

The streak is at twenty-seven days. More useful than the number is that scaling the loop to a pool found its
binding constraint, people, and could not lift it: every piece made that constraint visible and priced, and
none could supply the people who care to look.
