# A Build Through the Loop (v1)

This file runs one synthetic build all the way around the review-and-handoff loop, from the bar it
must meet to the number its review produces. Week 2's map,
`integration/week-02-review-and-handoff-loop.md`, named this exact gap: there was no worked example of
a build going all the way around the loop, only the questions each stage asks. This file closes it by
walking a single build through all five stages in order, including the part where the first review
sends it back. Everything here is synthetic: the build, the sheet, the invoices, the review outcomes,
and the numbers are made up to show the path. The two roles are the builder and the reviewer, never
real people, companies, or vendors. This file does not copy the five documents it moves through. It
references them by path and shows the build passing through each one.

The build goes around the loop twice. The first trip ends in a send-back. The second trip ends in an
approval. Tracing both is the point, because a path is only a loop if a send-back returns along the
same route it left on, and this build does.

## The synthetic build

The build is named `invoice-reminder-sheet-to-slack`. Every weekday morning it reads a Google Sheet of
open vendor invoices, finds the ones due in three days, and posts one Slack reminder per invoice to a
team channel. Each reminder carries the vendor, the amount, and the due date. That is the whole job: a
scheduled read, a filter to due-in-three, and one outbound message per matching row. It is the kind of
build the loop is built for, useful enough to run daily and simple enough to walk end to end.

## Stage 1: Set the bar

Before the build moves anywhere, there is a baseline it has to meet, and it is the same baseline for
the builder and the reviewer. That bar is `standards/automation-standards.md`. The builder does not get
to pick which sections apply. This build reads a sheet, posts to a channel on a schedule, and can be
re-run by hand, so the sections that bite are the ones about a scheduled, unattended job that writes to
a channel.

Section 2 (error handling), section 3 (retries and backoff), section 8 (ownership), and section 9
(change and rollback) all apply, and the builder does prepare each: an error path, capped retries on
safe steps, a named owner, and a versioned definition with a safe stop. The section that decides this
build's first review is section 4, idempotency. The standard states it plainly: "running the same input
twice should not create two of anything," and for outbound messages, "dedup on a content key within a
time window so a re-run does not double-notify." This build posts to a channel and can be re-run by
hand, which puts idempotency squarely on the list, and that is where this build fails its first review.

## Stage 2: Prep against the bar (trip one)

The builder runs `enablement/builder-self-check.md` top to bottom before handing anything off. Most of
it comes back clean, and honestly so.

- Section 1, run it yourself first: the builder ran the happy path with a real-shaped sheet and watched
  one reminder post for each invoice due in three days. The builder also ran a failure input, a row
  with a broken date, and confirmed the build skipped it and surfaced the problem to a human channel
  instead of posting a garbage reminder. The error path exists and tells a person.
- Section 2, make it safe to run: the Slack and Sheets credentials are in the credential store, scoped
  to what the build needs, with the environment suffixed.
- Section 3, make it operable by someone else: one owner is named next to the build, a single person
  rather than "the team." The safe stop is a disable toggle on the schedule that halts it cleanly. The
  rollback is a versioned export of the workflow, so a bad change can be reverted to a known-good
  version.
- Section 5, make it legible: the one-paragraph "what this does and why" is written.

There is no model call, so section 4 of the self-check (if your build calls a model) is marked not
applicable.

One item is where the trip goes wrong. Section 1 asks the builder to "run the same input twice and
confirm you do not get two of anything." The builder read the build, saw that it posts one message per
matched row, and marked this item as fine by eye, without actually running the same day through twice.
The reasoning felt safe: one row, one post. What the builder did not trace is that the Slack post step
retries on error, the daily schedule can overlap a manual re-run, and the post carries no dedup key.
Nothing stops the same invoice from being reminded twice. The one item the builder eyeballed instead of
running is the one real gap in the build. This is the blindness the self-check's own closing section
warns about: the builder is close to the build and reads past the gap they already assume is fine.

## Stage 3: Hand it off and its packet (trip one)

With the self-check marked clean, the builder assembles the handoff packet and crosses the handoff
point in `sops/hand-off-a-build-for-review.md`. The packet is the whole message across the seam, and it
is the three things that SOP requires.

1. The runnable build itself, the `invoice-reminder-sheet-to-slack` workflow with its sample sheet, in
   a form the reviewer can open and run.
2. The one-paragraph description: "Every weekday morning this reads the open-invoices sheet, finds
   invoices due in three days, and posts one Slack reminder per invoice to the team channel with the
   vendor, amount, and due date. It exists so nobody has to scan the sheet by hand to catch invoices
   before they slip."
3. Confirmation that the self-check is clean, including that the build was run against one good and one
   failing input, with an owner named and a rollback plan (the versioned export plus the disable
   toggle) in place.

The packet is complete on its face, so the handoff is accepted and the reviewer takes over. This is the
seam the loop depends on. Everything downstream now runs on the packet, including the one claim inside
it that the builder confirmed by eye rather than by running.

## Stage 4: Run the gate and decide (first review)

The reviewer runs `sops/run-a-build-review.md` against the build and fills in
`governance/ai-build-review-checklist.md`. This is where the gap surfaces, because the reviewer does
the thing the builder skipped.

- Read the description. Present and clear. The reviewer has a goal to check against.
- Run the happy path. The good sample sheet goes through and produces one reminder per due-in-three
  invoice. Matches the description.
- Run the failure input. The broken-date row is skipped and surfaced. Good.
- Walk the checklist top to bottom. Most Basics pass: the name says what it does, the steps are named,
  there is an error path, a person gets told on failure, secrets are in the credential store. Then the
  reviewer reaches the Basics line "running the same input twice does not create two of anything."
  Rather than reading the build and reasoning about it, the reviewer runs the same day through twice.
  Two identical Slack reminders land in the channel for every invoice: same vendor, same amount, same
  due date, posted twice.

That is a failed basic check. The reviewer checks why: the Slack post retries on error and has no dedup
key, and a manual re-run overlaps the schedule, so the same invoice id and due date post again. Section
4 of the standard is explicit that outbound messages must dedup on a content key. Per the decision rule
in the reviewer SOP, a failed basic check is a Send back. The reviewer marks the outcome and writes one
reason in the checklist:

> Send back. Re-running the same day double-posts a second identical reminder for every invoice. The
> Slack post is not idempotent, because it retries on error and has no dedup key, and a manual re-run
> can overlap the schedule. Add a dedup on a key of invoice id plus due date within the day so a re-run
> does not double-post (standard section 4, idempotency). Everything else passed.

The filled-in checklist is the whole message back. It travels to the builder along the same path the
packet came in on, carrying the outcome and the single reason, so nothing has to be re-explained.

## Stage 2 again: the fix and an honest re-run (trip two)

The build re-enters the loop at the self-check, exactly where `sops/hand-off-a-build-for-review.md`
says a send-back re-enters. The builder reads the returned checklist, which is now the to-do list, and
makes the fix the reason names: a dedup on a key of invoice id plus due date within the day, so a post
that has already gone out for a given invoice and due date on a given day is not sent again. This is
standard section 4 done properly, a content key within a time window.

Then the builder re-runs `enablement/builder-self-check.md`, and this time runs the same-input-twice
item instead of eyeballing it. First run: one reminder per invoice. Second run of the same day: no new
posts, because the dedup key already matches. The item that was marked by eye on trip one is now a real
yes, confirmed by running. That is the difference the send-back bought. The builder rebuilds the packet
(the fixed build, the same description, the clean self-check) and hands off again at the same handoff
point.

## Stage 3 and 4 again: hand off and approve (trip two)

The reviewer runs the same review SOP and fills the same checklist. Happy path: one reminder per
invoice. The re-run-twice check now holds: no second post. The Basics, ownership, and lifecycle checks
all pass. The one thing the reviewer flags is small: the reminder wording reads a little stiff and could
name the due date more plainly. That is a small, clearly listed fix rather than a failed check, so the
decision is Approve with fixes. The reviewer writes the one wording tidy-up in the checklist. The
builder makes that tidy-up, confirms it, and the build ships. Per the SOP, a small fix does not need a
second full trip through the loop.

The loop ran twice for one build. Trip one left as a packet and came back as a Send back checklist.
Trip two left as a packet and came back as an Approve with fixes checklist. Both trips used the same
handoff point and the same packet shape, which is what makes this a loop and not two separate processes.

## The number

Now measure it, using `analytics/metric-definitions.md`. This build was one handoff: one build
submitted for review, so it adds one to the denominator. Its first review landed on Send back, so it
adds one to the first-review send-back numerator for the period. That the second review approved it does
not change the count. The metric is explicit on this: "a build that is sent back, fixed, and re-reviewed
still counts once here, as one send-back, so a rough build cannot quietly improve the rate by coming
around the loop again."

So for a period in which this was the only handoff, the send-back rate is 1 / 1. If it sat in a week of,
say, 8 handoffs where it was the only first-review send-back, the rate is 1 / 8. Either way, this build
contributes its first-review outcome, not its final one. The send-back rate reads trip one's result and
ignores that trip two approved. That is the rule working as intended: the number measures whether the
build arrived review-ready the first time, and this one did not, because the builder eyeballed the
idempotency item instead of running it. The fact that this build eventually shipped does not erase that
it arrived not-ready and bounced. The metric points back at stage 2, the self-check, which is exactly
where the fix lived. A sharper self-check is the answer here, not a stricter review.

## What this shows and what it does not

This shows the loop runs. A build met a bar, got prepped, crossed a handoff point in a packet, hit the
gate, was sent back for a real and specific reason, came back around the same path, was approved with a
small fix, and produced a number that counted the first outcome the way the metric says to. The five
pieces move a build from done to shipped as one path, the send-back returned along the same route it
left on, and the seams held.

It does not prove the loop is complete. This is one synthetic trip with one planted flaw, chosen because
it is a clean example of a failed idempotency check. A real build can fail in ways this trace never
touches: a missing owner, a secret typed into a step, a retry on a genuinely unsafe write, an error path
that goes to a channel nobody reads. This example also assumes an honest reviewer who actually runs the
day twice. A reviewer who eyeballs the same item the builder eyeballed would have approved the
double-post, and the send-back rate would have missed it entirely. That gap, whether the review itself
is real, is still open, the same one the week 2 map named. And one trip around says nothing about a
queue of builds waiting on one reviewer, where the next bottleneck usually shows up. One trip around
proves the path exists. It does not prove the path catches everything.

---

*v1. A living example. The next pass runs a second synthetic build with a different flaw, an ownership
or a secrets miss rather than an idempotency one, so the trace shows the loop catching more than one
kind of miss, and adds the handoff-log row this build would have produced.*
