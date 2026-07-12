# Week 3 Log

Days 015 to 020. Week 1 was breadth and week 2 was depth, both of them on paper. This week's job was to
make the loop real and turn it on itself: run one synthetic build through last week's review-and-handoff
loop to see the spot it rests on, then wrap a second loop around that spot. Audit the reviewer the run
leans on, keep the miss it turns up a calibration, spec the log the audit and the count both read, define
the second metric that watches the first, and then map the five as one loop. Six days, six artifacts, one
loop wrapped around last week's review stage.

## What shipped

- `examples/a-build-through-the-loop.md`: v1, one synthetic build run all the way around the week-2 loop
  twice, a planted idempotency flaw caught on a first-review send-back and approved on the second, closing
  on the note that the loop rests on an honest reviewer. Adds a new `examples/` folder.
- `governance/review-spot-audit.md`: v1, a spot-audit where a non-reviewer re-reviews a small random
  sample of already-decided builds (weighted toward approvals), a different decision is a miss, read next
  to the send-back rate.
- `enablement/handling-a-review-miss.md`: v1, how to run the auditor-reviewer conversation so a miss stays
  a calibration, not a charge.
- `sops/review-log-spec.md`: v1, one row per handoff (build, reviewer, first-review outcome, date), the
  record the audit samples and the metric counts, closing the reviewer-field prerequisite the audit named.
- `analytics/metric-definitions.md`: to v3, the review miss rate, the share of audited reviews the audit
  overturned, the second signal read next to the send-back rate and a detector on an approval-weighted
  sample.
- `integration/week-03-the-loop-watching-itself.md`: v1, the five pieces mapped as one loop that watches
  week 2's review stage and closes the gap week 2 named.

## What I actually learned

Two weeks of this repo described a loop. Day 015 ran one build through it, and that is a different claim.
Reading the pieces, each one looked correct on its own. Carrying a single build from the bar it must meet
to the number its review produces is what proved they actually connect, that a decision made at the
review comes back down the seams to the builder and the send-back rate counts the right outcome. The move
that taught me the most was planting a real flaw and letting the loop catch it, instead of walking a
clean build straight to approval. A build that sails through proves nothing. The send-back is where you
find out the seams carry a decision back. Documented and demonstrated are different claims, and only the
second one survives contact with a build.

The rest of the week was one move, and it is the move I keep relearning. The worked example exposed the
loop's one open assumption: the whole thing rested on the reviewer actually running the checks, and
nothing checked the reviewer. So I built a control pointed at the review, a spot-audit that re-reviews a
sample of decided builds by someone who was not the original reviewer. What I had to accept while
building it is that this relocates trust rather than removing it, one ring further out. Week 2 asked me to
trust the builder's word that a build was ready. The review replaced that with the reviewer's word that
they checked. This week replaces the reviewer's word with a record a second person can sample. The word
keeps moving out a ring, and it never fully goes away: there is always an outer edge, an auditor nobody
audits, taken on faith. You cannot reach zero trust. You push the trusted spot to where abusing it is
cheapest to detect, so a careful pass is the easier path, and that is all a control ever buys you.

The last thing the week taught is that governance builds the mechanism and enablement decides whether it
survives contact with people. The spot-audit is a clean design on paper. It is only as good as the
conversation a miss triggers. Deliver a miss as a charge, and the reviewer's rational move is to stop
making real calls, to rubber-stamp everything or send everything back, which destroys the exact signal
the audit was built to protect. A control that punishes the honesty it depends on gets that honesty
withdrawn. I can design a correct audit and still kill it in the first conversation, because the people
layer is where the mechanism lives or dies.

## What was thinner than I wanted

All of it is still synthetic and on paper. One worked example with one planted flaw, no real reviews, no
real audits, and no real miss conversation that tested whether a miss stays a calibration when it lands
on a specific person who reads it as a charge. The path is drawn. It has not been run against a build
anyone actually cared about.

The outer edge still runs on trust. The audit watches the reviewer, and nothing here watches the auditor
except rotation and a cadence someone has to keep, so the last ring is a person no control here reaches.
That is the ceiling built into the design, and naming it does not close it.

The numbers are shapes without data. The review log is a spec, not a running log, so the review miss rate
is defined but has no filled rows to compute from, and the send-back rate still has one synthetic row
behind it. And the loop still covers one build and one reviewer at a time, so the reviewer-queue
bottleneck week 2 named is still open: nothing here says what happens when builds arrive faster than one
reviewer clears them, or one auditor.

## Carrying into week 4

- Run a real spot-audit against a filled review log, so the review miss rate has data behind it instead
  of a defined shape.
- Take on the reviewer-queue bottleneck that week 2 and week 3 both named: what happens when builds arrive
  faster than one reviewer clears them.
- Trace a second worked build whose miss is a rubber-stamped approval, not an honest send-back, since that
  is the miss the audit exists for and the one this week's example did not show.

The streak is at twenty days. More useful than the number is that the loop stopped being only described
this week and got run once, then a second loop closed around the spot that run exposed, which is the
difference between writing a system down and watching it work.
