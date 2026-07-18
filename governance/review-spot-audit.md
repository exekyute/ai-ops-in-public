# Review Spot-Audit (v1)

The review-and-handoff loop puts a guardrail on the builder. The review checklist
(`governance/ai-build-review-checklist.md`) and the reviewer SOP (`sops/run-a-build-review.md`) exist
so a build is checked by someone other than the person who made it, and the send-back rate
(`analytics/metric-definitions.md`) counts how often that check bounces a build. Nothing in the loop
does the same for the reviewer. The loop assumes the review itself was honest, and a reviewer who waves
everything through drives the send-back rate toward zero until the number stops meaning anything. This
file is the guardrail on the reviewer, the way the checklist is the guardrail on the builder: a
spot-audit, where a small random sample of already-decided builds gets re-reviewed by someone who was
not the original reviewer, so a lazy review becomes detectable instead of invisible.

## Why this exists

Every control in the loop points at the builder. The builder self-check
(`enablement/builder-self-check.md`) is the builder grading their own prep. The review checklist is a
second person grading the build. The send-back rate counts how often that second person had to bounce
one. All three assume the second person actually ran the review.

That is the trust-relocation problem. A control that checks the builder but not the reviewer moves the
trust up one level instead of removing it, from the builder to the reviewer. You have traded "trust the
builder's word that the build is ready" for "trust the reviewer's word that they checked." The word
moved. It did not go away.

Day 015's worked example (`examples/a-build-through-the-loop.md`) made this concrete. The builder
eyeballed the idempotency item instead of running it, and the review caught the double-post only because
the reviewer actually ran the same day through twice. A reviewer who eyeballed the same item the builder
eyeballed would have approved the double-post, and the send-back rate would never have seen it. The week
2 map (`integration/week-02-review-and-handoff-loop.md`) named the same gap: the loop assumes an honest
reviewer, and a reviewer who waves everything through drives the send-back rate to zero.

So the send-back rate needs a second signal beside it, because on its own it cannot separate two cases
that read the same from the number:

- A near-zero send-back rate because builds genuinely arrive ready. Real prep.
- A near-zero send-back rate because the reviewer approves everything without looking. A rubber stamp.

The spot-audit is that second signal. A near-zero send-back rate with clean audits is real prep. A
near-zero send-back rate with audit misses is a rubber stamp. Read the audit next to the send-back rate,
never the rate on its own. Neither one answers the question alone.

## What a spot-audit is

A spot-audit is a re-review of an already-decided build, done by a second person who was not the
original reviewer and not the builder. The auditor re-runs the normal review: the reviewer SOP
(`sops/run-a-build-review.md`) against a fresh copy of the review checklist
(`governance/ai-build-review-checklist.md`), with the same three outcomes on the table, Approve, Approve
with fixes, or Send back. The audit reuses the review checklist rather than replacing or duplicating it.
It runs the same checklist again, cold, on a build that already carries a decision, to see whether a
second honest pass lands in the same place.

A miss is when the audit reaches a different decision than the original review. The one that matters most
is an approval the audit would have sent back: the original reviewer waved through a build that a real
review should have bounced. That is the rubber stamp leaving a mark. A miss in the other direction (the
original sent back a build the audit would have approved) is worth a conversation too, but the false
approval is the one the send-back rate cannot see, so it is the one the audit is built to catch.

The sample must include approvals and approve-with-fixes. A lax reviewer's damage hides in the builds
that were waved through, not in the ones that were sent back. If you only audit send-backs, you audit the
one pile where the reviewer was already paying attention. Weight the sample toward the decisions where a
miss would be invisible: the approvals.

## How to run one

1. **Pick a small random sample.** From the builds decided since the last audit, draw a few at random,
   not by picking the ones that look off. Keep it small. Weight the draw so it includes approvals and
   approve-with-fixes, because that is where a lax review does its damage. A sample that is all
   send-backs tells you nothing about the builds that shipped.

2. **Re-review blind first.** For each sampled build, run `sops/run-a-build-review.md` against a fresh,
   empty `governance/ai-build-review-checklist.md`, without reading the original marks. Put the good
   input and the bad input through it yourself, walk the checklist top to bottom, and land on your own
   decision the way the first reviewer was supposed to. Blind first, so the original decision does not
   anchor yours.

3. **Compare to the original.** Open the original filled-in checklist and set it next to yours. Same
   decision, or different? If different, find where: which check did one of you mark differently, and
   why.

4. **Record any miss.** If the audit reached a different decision, write down the build, the original
   outcome, the audit outcome, and the one check that split them, the same shape a normal review already
   produces. An approval the audit would have sent back is the miss that matters most. One miss is a
   record, not yet a verdict; a pattern across audits is the signal.

## Who runs it and how often

The auditor is a third role, separate from the two the review already has: not the builder, and not the
reviewer who made the original call. If the auditor reviewed the build the first time, they are grading
their own review, which is the exact thing the audit exists to catch.

Rotate so nobody audits their own reviews. Section 8 of `standards/automation-standards.md` already
treats ownership as a named, accountable responsibility with an explicit handover when the owner changes,
and the same idea applies to the auditor role. The audit is a job someone owns for a stretch, and it
moves, so the person who reviewed a build is not the person who audits it. An auditor who always audits
the same reviewer, or who is never audited in turn, becomes the new unchecked spot.

Set a cadence and keep it. Small and regular beats big and rare. A few builds re-reviewed every couple of
weeks keeps a lazy review detectable on a short horizon. A large audit once a quarter is easy to see
coming and easy to prep for, and it tells you about builds that shipped months ago, too late to correct
the habit. Pick a cadence you will actually hold, and hold it.

## What a miss means and what it does not

A miss is a calibration signal, a place where two reviews of the same build disagreed. Treat one miss as
a conversation, not a charge. Reviews are judgment calls, and two careful people can land differently on
a single build, especially on the line between approve-with-fixes and send-back. Sit down, work out which
reading matches the standard, and move on. Sometimes the audit is the one that got it wrong.

A pattern is different. One reviewer whose approvals keep coming back as audit misses, on checks that are
not close calls, is a reviewer whose approvals do not hold up. That is what the audit is for: to turn a
hunch about a rubber stamp into a record you can point at.

Read a miss next to the send-back rate, always. The rate tells you how often builds bounce; the audit
tells you whether the approvals behind a low rate are real. Neither is enough alone.

## What this does not do

Be honest about the limits. The audit buys detectability, not a guarantee.

- **The auditor is also a person.** An audit is another review, run by someone who can also be lazy,
  rushed, or wrong. Rotation and a set cadence raise the cost of that, and they do not remove it. The
  audit makes a bad review detectable. It does not make one impossible.
- **A small sample can miss.** If you audit four of forty approvals, a single bad approval can sit in the
  thirty-six you did not pull. The audit lowers the odds that laziness pays off over time. It does not
  drive them to zero, and one clean audit does not certify a reviewer.
- **Auditing everything would just move the problem.** The audit is partial on purpose. Audit every
  review and you would need someone to trust the auditors, and the trust problem climbs one more level
  with nothing gained. The point is to make a lazy review detectable and raise its cost, so a careful
  review is the easier path.
- **It makes laziness detectable, not impossible.** That is the honest ceiling. A reviewer who wants to
  cut corners still can. The audit means a rubber stamp can be seen, priced, and named, instead of hiding
  forever behind a send-back rate of zero.

## What comes next

Two threads this guardrail named have since been picked up, and one gap now sits under both.

The miss count wants its own metric. Right now a miss is a note you read by hand. Counted properly it
would be a review miss rate, the share of audited reviews whose decision the audit overturned, defined in
`analytics/metric-definitions.md` the way send-back rate is, with its own formula, what counts, and how
to read it without fooling yourself. That is the number you read next to the send-back rate instead of a
pile of notes. It has since been defined (`analytics/metric-definitions.md`); what stays open under it is
data, since no real audit has filled it yet.

An audit also needs a review log to sample from. The send-back rate already draws on the review records
for one row per handoff: the build, its first-review outcome, and a date
(`analytics/metric-definitions.md`). The audit draws on those same records, and it needs one more field
on them, the original reviewer. Without the reviewer written down, you cannot reliably hand a build to
someone who did not review it, and you cannot tell whether one reviewer's approvals keep coming back as
misses. That reviewer field now sits in the review log spec (`sops/review-log-spec.md`), which pins down
one row per handoff with the reviewer included, the field this audit named as its prerequisite, so the
audit has a defined shape to sample from. What stays open is the same gap as above: the spec is written,
and no real queue has filled it with rows.

---

*v1. A living guardrail. It checks the reviewer the way the checklist checks the builder. The review miss
rate and the review log it named have both been defined since; the next pass runs a real spot-audit
against a filled log so the miss rate finally has data behind it.*
