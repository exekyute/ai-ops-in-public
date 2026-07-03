# Metric Definitions (v2)

A number is only useful if everyone reading it counts the same thing. This file defines the
metrics this lab uses to tell whether an automation is actually working, and whether the builds
behind it arrive ready for review, one entry at a time.
Each entry pins down what the metric is, the exact formula, what counts and what does not,
where the data comes from, how often to read it, and the ways the number can mislead you.

The rule for adding a metric here: if you cannot compute it by hand from a sample of the records
it draws on (run logs, review records, whatever the metric counts), it is not defined well enough
to belong yet. All examples use synthetic data.

## Exception rate

**What it is.** Of all the times an automation ran in a period, the share that did not finish
on their own. An exception is any run that ended in an error, or that had to be handed to a
person to decide or fix before it could complete. The rest are straight through: started,
finished, no human needed.

**Why it matters.** It is the most honest health signal an automation has. A workflow can look
impressive and still be mostly manual underneath. If one run in three falls out to a person,
the automation is doing less of the work than the demo suggested, and you want to know that
before you call it done.

**Formula.**

    exception rate = exceptions / total runs

**What counts.**

- *Total runs* is every run started in the period, including the ones that failed. Count
  attempts, not just successes, or the rate will flatter you.
- *Exceptions* is a run that either ended in an error state, or was routed to a person to
  resolve. Decide per workflow what "routed to a person" means and write it down next to the
  build, so the count does not drift over time.
- A run that retried on its own and then finished is not an exception. The point is whether a
  human had to step in, not whether the first attempt was clean.

**Where the data comes from.** The execution or run log of the tool itself. You need, at a
minimum, one row per run with a final status and a timestamp. If the log cannot tell you
whether a run finished on its own, that is the first thing to fix, because nothing here is
measurable until it can.

**How often to read it.** Weekly per workflow is enough to see a trend without chasing noise.

**How to read it without fooling yourself.**

- *Watch the volume.* A 30 percent rate on 10 runs is one bad afternoon, not a pattern. Put the
  run count next to the rate, every time.
- *Segment by reason.* A single rate hides the cause. The fix for "the input was malformed" is
  not the fix for "the model's answer needed a human check," and one number cannot tell them
  apart.
- *Mind the runs that never start.* A run that silently fails to trigger never lands in the
  log, so it never counts as an exception. A falling rate can mean the work is getting cleaner,
  or it can mean fewer runs are firing at all. Check the volume before you celebrate.

**A worked example (synthetic).** A weekly intake automation ran 120 times. 12 ended in errors,
and 18 were handed to a person to fix a field before they could continue. Exceptions are 30, so
the exception rate is 30 / 120, or 25 percent. Three in four ran straight through. Next to that
you would note the count (120) and the split (12 errors, 18 human fixes), because the 18 is
where the next improvement probably lives.

**On targets.** There is no universal good number. Set a threshold per workflow based on what
it does and what a fallout costs, then watch the trend more than the absolute value. A rate
that drifts up week over week is a problem even if it is still low.

## Send-back rate

**What it is.** Of all the builds handed off for review in a period, the share the reviewer sent
back on the first review instead of approving. A handoff is one build submitted for review, and its
first review lands on exactly one of three outcomes: Approve, Approve with fixes, or Send back (see
`sops/run-a-build-review.md`). A send-back is the "Send back" outcome: the build was not ready and
returned to the builder with a to-do list. This is not the exception rate. Exception rate is a
runtime signal, the share of a live build's runs that errored or fell out to a person. Send-back
rate is about the step before that, the handoff itself: before a build is approved, does it arrive
review-ready, or does it bounce back to the builder. A build can post a clean exception rate later
and still have been sent back twice before it went live, and this is the number that catches that.

**Why it matters.** It tells you whether the builder self-check is actually working. The self-check
in `enablement/builder-self-check.md` exists so a build reaches the reviewer already ready: an owner
named, a rollback in place, and both a good and a bad input already run. When the self-check is
doing its job, most handoffs pass on the first try and review is a quick confirmation. When the
send-back rate is high, builds are arriving half-ready and the review is absorbing work the
self-check was supposed to clear. That is a prep problem, not a review problem, and this number is
how you see it.

**Formula.**

    send-back rate = first-review send-backs / handoffs reviewed

**What counts.**

- *Handoffs reviewed* is every build that was handed off and got a first review in the period, one
  handoff per build submitted. Count the ones that came back too, or the rate will flatter you.
- *First-review send-backs* is the numerator: a handoff whose first review landed on "Send back."
  Count the first review only. A build that is sent back, fixed, and re-reviewed still counts once
  here, as one send-back, so a rough build cannot quietly improve the rate by coming around the loop
  again (see `sops/hand-off-a-build-for-review.md`).
- The two passing outcomes, "Approve" and "Approve with fixes," both count as a first-pass pass.
  "Approve with fixes" is a pass because the build ships once small listed fixes are done; it did not
  bounce back to the builder to rebuild. Only "Send back" counts against the rate.
- The complement is the first-pass approval rate: (handoffs reviewed minus send-backs) / handoffs
  reviewed, the share that passed on the first try. Send-back rate and first-pass approval rate sum
  to 1. Lower send-back rate is better, which reads the same direction as exception rate, where
  higher is worse. Higher first-pass approval is better.
- Only builds that were actually handed off count. A build a builder keeps self-checking and never
  submits never enters review, so it never lands in the numerator or the denominator.

**Where the data comes from.** The review records, not the execution logs. Each first review
produces a filled-in `governance/ai-build-review-checklist.md` with one of the three outcomes marked
and the reasons written, and that filled checklist is the message that travels back to the builder,
so it is the record this metric counts. Review outcomes do not live in a tool's run log; a run log
knows whether a live automation finished, not whether a build passed review. You need one row per
handoff: the build, the first-review outcome, and a date. A short handoff log that lists each
submission and its first outcome is enough. If reviews are decided verbally and no checklist is
filled, or you cannot tell a first review from a re-review, that is the first thing to fix, because
the numerator depends on it.

**How often to read it.** Weekly is enough to see whether prep is holding without chasing noise, the
same cadence as exception rate, as long as the count is large enough to mean something. In a slow
week of two or three handoffs, read it monthly instead, or read the raw counts and skip the rate.

**How to read it without fooling yourself.**

- *An honest review is the whole assumption.* A reviewer who approves everything to avoid friction
  drives the send-back rate to near zero, and then it measures nothing. The number is only as real
  as the review behind it. A suspiciously perfect rate is a reason to check the reviews, not to
  celebrate.
- *Watch the volume.* A 25 percent rate on 4 handoffs is one bad week, not a trend. Put the handoff
  count next to the rate, every time.
- *"Approve with fixes" is a soft pass, not a clean one.* It counts as a first-pass pass here, but it
  shipped with a fix-list, which means the self-check missed something. Track clean Approves (an
  "Approve" with no fixes) as a separate number, so a pile of soft passes does not hide behind a
  healthy-looking rate.
- *This says nothing about work that never ships.* Only handoffs count. A build that gets
  self-checked forever and never submitted never lands in the denominator, so a low rate can sit
  next to a stack of builds nobody ever handed off. A falling rate can mean prep improved, or it can
  mean fewer, safer builds are being submitted at all. Check the handoff count before you read it as
  progress.

**A worked example (synthetic).** In one week, 40 builds were handed off and got a first review. On
that first review, 10 were sent back, so the send-back rate is 10 / 40, or 25 percent. The
complement is the first-pass approval rate, 30 / 40, or 75 percent, and the two sum to 100 percent.
Of the 30 that passed, 18 were a clean "Approve" and 12 were "Approve with fixes." Next to the 25
percent you would note the count (40) and the split (18 clean, 12 soft passes, 10 send-backs),
because the 12 soft passes are where a healthy-looking rate can be hiding work the self-check still
missed.

**On targets.** There is no universal good number, and zero is a warning sign, not a goal, because
it usually means the reviewer is waving builds through. Set a threshold from your own baseline once
you have a few weeks of honest reviews, leave room for real send-backs, then watch the trend more
than the absolute value, and read it alongside the clean-approval share. A rate that drifts up week
over week means prep is slipping even if it is still low; a rate that snaps to zero means the review
stopped being real.

## What changed in v2

- Added "Send-back rate": the share of handed-off builds a reviewer sends back on the first review,
  the metric for whether the builder self-check is arriving review-ready, framed against its
  complement, first-pass approval rate, and kept distinct from exception rate.
- Broadened the opening scope line and the adding rule to cover metrics that come from review
  records, not just run logs, now that a second metric draws on the review side.

---

*v2. A living dictionary. Each later pass adds a metric or sharpens one once a real read of the
data showed where it was vague.*
