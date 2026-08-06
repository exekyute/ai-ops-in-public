# Handoff Intake (v1)

Everything else in this repo describes how a finished build reaches a reviewer. This runs it.

[The handoff SOP](../../sops/hand-off-a-build-for-review.md), the documented path a build travels from
the person who made it to the person who reviews it, has three steps on the builder's side: finish the
self-check, assemble the packet, hand it off. It also states a rule with teeth, that a partial packet is
not a handoff and must not be sent with the rest promised later. Until now that rule was enforced by
whoever remembered it.

[`workflow.json`](workflow.json) is an n8n workflow that enforces it instead. A builder submits the
packet through a form, the submission is checked against what the SOP requires, and only a complete one
opens a row in the review queue. An incomplete one is returned immediately with the list of what is
missing.

![The handoff intake workflow on the n8n canvas: a form trigger feeds a code node that checks the packet, then an IF splits into an accepted branch that opens a queue row, notifies the reviewer pool and confirms the handoff, and a returned branch that records the attempt and hands it back to the builder.](canvas.png)

The branch is the whole file. Everything above the split is reading what was submitted; everything after
it is the SOP's rule about partial packets, running.

## What it does

1. **Receive a handoff packet.** A form collecting exactly what
   [the SOP's packet section](../../sops/hand-off-a-build-for-review.md) requires: the build name, who
   built it, somewhere the reviewer can open and run it, the one-paragraph description of what it does
   and why, one named owner, a rollback plan, and confirmation that the build was run against a good
   input and a failing one.
2. **Check the packet against the SOP.** A Code node that re-checks every field server-side and builds
   a plain-language list of what is missing. It does not trust the form's own required flags.
3. **Is the packet complete?** The branch that makes the rule real.
4. **Accepted:** open one row in the `review_queue` table carrying the handoff time, notify the reviewer
   pool, and confirm to the builder.
5. **Returned:** record the attempt, and hand the builder the exact list of what was missing.

## The decision worth explaining

It writes **one** record, not two.

The obvious design opens a review-log row and a queue row together. That is wrong here, and
[the review log spec](../../sops/review-log-spec.md), which defines what one row of the permanent record
holds, says why: write the row when the first review lands. Its **Handed off** field is explicit that the
queue row carries the handoff time while a build waits, and that the time is copied onto the log row as
the review is written.

So the handoff half of the loop opens a queue row and nothing else. The log row does not exist yet,
because no review has happened, and inventing one early would put a row in the permanent record with
three of its five required fields empty.

## Running it

1. Import `workflow.json` into n8n.
2. Create a Data Table named `review_queue` with nine string columns: `build`, `builder`,
   `build_location`, `description`, `owner`, `rollback`, `handed_off_at`, `status`, `reviewer`.
3. Attach a Slack credential to **Notify the reviewer pool** and point it at your own channel. The
   exported file carries no credential, so this is the one connection you have to make yourself.
4. Activate it, and hand the form URL to whoever builds.

It ships inactive. Nothing runs until you turn it on.

## Reviewed against this repo's own checklist

An automation in a repo about reviewing automations should go through the gate. It was run against
[the review checklist](../../governance/ai-build-review-checklist.md), the list a build passes before it
goes live, and the honest outcome is **Approve with fixes**, not a clean approve.

What passes: the name says what it does, every node is named for what it does rather than left as a
default, the workflow definition is versioned in this repo and revertible, there is a safe stop in the
activation toggle, no secret sits in any node parameter, expected failures are handled in logic rather
than raised as alerts, and the description and sticky notes travel with the build.

What does not, with the fix for each:

- **Running the same input twice creates two queue rows.** Section 4 of
  [the automation standard](../../standards/automation-standards.md), the bar every build here is judged
  against, asks that a repeat not create two of anything. This one has no dedup key. The subtlety is that
  a naive fix would break a different rule:
  [the handoff ruling](../../governance/what-counts-as-one-handoff.md) makes a re-submission a genuine
  second **arrival**, so a second queue row is correct in that case and wrong for a double-click. The fix
  is a submission id on the form, not deduplication on the build name.
- **A failed write tells nobody.** If the Data Table insert fails, the builder sees a broken form and no
  alert reaches a person. Section 2 requires the opposite. The fix is an error branch on both insert
  nodes routing to the same channel the reviewer pool watches.
- **One credential, no environment split.** Section 1 requires separate test and prod credentials with
  the environment suffixed. This has one Slack credential and no suffix.
- **Nothing tracks volume or exception rate.** Section 6 asks for both per workflow, and the
  [exception rate](../../analytics/metric-definitions.md) is defined for exactly this purpose. Nothing
  here reads the execution log yet.

The AI-steps section is marked not applicable, because this build calls no model. That leaves a gap this
repo has already named in writing and has still not closed: no worked example here traces a build that
calls one.

## What it does not do

It covers the builder's side of the handoff and stops at the queue. Assigning a reviewer, running the
review, writing the log row, and returning the decision are all still a person following
[the reviewer SOP](../../sops/run-a-build-review.md). Automating the intake does not make the review
happen; it makes an incomplete packet impossible to hand over quietly.

---

*v1. A living automation. The next pass adds the submission id, the error branch, and the first read of
its own execution count, then re-runs the checklist to see which lines actually moved.*
