# The Loop Watching Itself (v1)

This week shipped five pieces: a worked example, a spot-audit on the reviewer, a guide for the miss it
turns up, a review-log spec, and a new metric. On their own they read as five loose documents. Put in
order, they are the stages of one loop that watches another loop: run one build through last week's
review-and-handoff loop to see the spot it rests on, re-review the reviewer, keep the miss a
calibration, record it, and count it. This file is that map. It also wraps around one stage of last
week's map: what week 2 ran as "run the gate and decide" is the exact thing this whole loop watches.

## The loop

The review-and-handoff loop watches the build. This loop watches that loop's review, moving through the
same five stages each cycle, from the trust it exposes to the number that says whether the approvals
hold up.

1. **See where the loop rests on trust.** One synthetic build goes all the way around the week-2 loop,
   from the bar it must meet to the number its review produces, including the first trip that ends in a
   send-back. Its honest close names the loop's one open assumption: a reviewer who runs the checks
   instead of reading past them, since the send-back caught the build's double-post only because the
   reviewer ran the check the builder had eyeballed. Running the loop once is what makes that trust
   visible, so there is something specific to watch.
   *Piece:* `examples/a-build-through-the-loop.md`.

2. **Re-review the reviewer.** A small random sample of already-decided builds gets re-reviewed cold by
   someone who was neither the builder nor the original reviewer, weighted toward the approvals, because
   that is where a lax review hides. If the second pass lands on a different decision, that is a miss,
   and an approval the audit would have sent back is the rubber stamp leaving a mark. This is the
   guardrail on the reviewer, the way the checklist is the guardrail on the builder.
   *Piece:* `governance/review-spot-audit.md`.

3. **Keep the miss a calibration.** Finding the miss is all the audit can do; the conversation after it
   is what makes the next review sharper. Delivered as a charge ("you approved a bad build"), a miss
   turns the reviewer defensive, and a defensive reviewer stops judging builds, the exact rubber stamp
   the audit was built to catch. So the conversation names the kind of miss together (a judgment call,
   or a check read instead of run), settles the right call against the standard, and stays on the build.
   *Piece:* `enablement/handling-a-review-miss.md`.

4. **Record every review.** One row per handoff (the build, the reviewer, the first-review outcome, and
   the date), the shared record the audit samples from and the send-back rate counts. It adds the
   reviewer field the audit named as a prerequisite, so a build can be handed to someone who did not
   review it and one reviewer's approvals can be traced across audits, with the first-review outcome
   frozen once written.
   *Piece:* `sops/review-log-spec.md`.

5. **Measure and feed back.** The review miss rate is the share of audited reviews the audit overturned,
   the second signal read next to the send-back rate, so a near-zero bounce rate cannot pass a rubber
   stamp off as real prep. A high miss rate, or one reviewer's approvals that keep coming back as misses,
   says the approvals are not holding up and points the fix back at the review itself, the stage last
   week's loop ran as "run the gate and decide." That pointer back to the review is what makes this a
   loop and closes the ring.
   *Piece:* `analytics/metric-definitions.md`.

## The handoffs

Most of the value sits in the seams between the pieces, not in the pieces on their own.

- The **worked example** is what makes the **audit** necessary. Running one build all the way around the
  week-2 loop is what exposes the single spot the whole loop rests on: a reviewer who runs the
  same-input check rather than reading past it. Without the example naming that spot, the audit is a
  guardrail on a problem nobody located, so the example is what turns an abstract assumption into a
  target.
- The **audit** produces a **miss**, and the **miss conversation** is what a miss is worth. The audit
  can surface a disagreement between two reviews; it cannot make the next review sharper. That happens
  only in the conversation, so a miss handled as a charge sours the review it measures and blinds the
  audit that found it.
- The **audit** and the **metric** both read the **log**, and the log carries the field the audit named.
  The send-back rate reads the build, the outcome, and the date; the audit reads those plus the
  reviewer; the miss rate reads the audit fields. One row, three readers. The reviewer field is the seam
  that lets the audit steer a build away from its own reviewer, and the audit was waiting on it.
- The **log** is what the **miss rate** counts, and the frozen first-review outcome is what keeps both
  numbers honest. If a re-review overwrote the first outcome, a rough build could come around the loop
  and erase its own send-back, and an overturned approval could quietly rewrite itself. One row per
  handoff, first outcome frozen, is what stops both.
- The **miss rate** is what points back at the **review**. A high miss rate sitting under a low
  send-back rate says the approvals do not hold up, so the number sends you back to the reviewer, the
  way last week's send-back rate sent you back to the self-check.

## The loop in one line

Run one build around the loop to expose the trust it rests on, re-review the reviewer to make a lazy
review detectable, keep that miss a calibration so the check survives, log the one row both the audit
and the count read, and let the share of audited reviews the audit overturned tell you whether a low
bounce rate is real.

## Where this fits in the last two loops

Week 1's map, `integration/week-01-automation-lifecycle.md`, had "review it before it ships" as one
stage of the automation lifecycle. Week 2's map, `integration/week-02-review-and-handoff-loop.md`,
opened that one stage into its own full loop, from the bar a build must meet to the number that says
whether it arrived ready. And week 2 named its own open gap plainly: nothing measured whether the review
itself was real, so the whole loop rested on an honest reviewer, and a reviewer who waves everything
through drives the send-back rate to zero until the number stops meaning anything.

This week is the loop that closes that gap. Where week 2 watches the build, week 3 wraps a second loop
around week 2's review stage and watches the review, one ring further out. It is the
who-watches-the-watcher layer, the same five-stage shape aimed one level up: an example that exposes the
trust, an audit that watches the reviewer, a guide that keeps the audit survivable, a log both read, and
a number that points back at the review. Say it plainly: week 2 named the gap, an unwatched reviewer,
and week 3 built the loop that closes it.

Be honest about what wrapping a loop around the reviewer buys. It pushes the trusted spot out one ring;
it does not remove it. Week 2 asked you to trust the builder's word that a build was ready, and the
review replaced that with the reviewer's word that they checked. This week replaces the reviewer's word
with a record a second person can sample. The word keeps moving out a ring, and it never fully goes
away: there is always an outer edge, an honest auditor nobody audits, and auditing every review would
only move that edge one more level up with nothing gained (per `governance/review-spot-audit.md`).
Rotation and a held cadence raise the cost of a lazy audit, and they do not drive it to zero. The point
of the ring is to make a rubber stamp detectable and priced, so a careful review is the easier path, not
to reach a level with no trust left in it.

## What is still missing

Each piece is a v1, with the metric now at v3, and this map is a v1 too. A real program would close gaps
this map still has. The outer edge still runs on trust: the audit watches the reviewer, and nothing here
watches the auditor except rotation and a cadence someone has to keep, so the last ring is a person
taken on faith. The review log is a spec, not a running log, so the review miss rate is defined but has
no filled rows with audit fields to compute it from, and the send-back rate has exactly one synthetic
row behind it; both numbers are shapes without data. This loop still covers one build and one reviewer
at a time, so the reviewer-queue bottleneck week 2 named as still missing is still open, and it says
nothing about a queue of builds waiting on one reviewer or one auditor. And all of it is synthetic and
on paper: one worked example with one planted flaw, no real reviews, no real audits, no real miss
conversation that tested whether a miss stays a calibration when it lands on a specific person. The path
is drawn. It has not been run against a build someone actually cared about. Those are the threads the
coming weeks pull on.

---

*v1. A living map. The next pass runs a real spot-audit against a filled review log so the review miss
rate has data behind it, and traces a second synthetic build whose miss is a rubber-stamped approval
rather than an honest send-back.*
