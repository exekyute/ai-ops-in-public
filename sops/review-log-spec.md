# The Review Log (v3)

Two documents in this repo already lean on a record they never define. The send-back rate
(`analytics/metric-definitions.md`) counts one row per handoff: the build, the first-review outcome, and
a date. The spot-audit (`governance/review-spot-audit.md`) samples from those same rows, and it named one
more field it needs, the original reviewer, as a prerequisite it is still waiting on. This spec is that
record. It defines one review log both can draw on, so the metric and the audit read the same rows instead
of two half-described ones.

## Why a log, not scattered checklists

Every review already produces a full record. When a reviewer runs `sops/run-a-build-review.md`, they fill
in `governance/ai-build-review-checklist.md`, mark each check, write the reasons, land on a decision, and
file that checklist with the build. That filled checklist is the complete account of one review, and it is
the right artifact for reading what happened on a single build.

What it cannot do is answer a question that spans many reviews. To ask "what share of handoffs bounced
this month," you would have to open every filed checklist and tally them by hand. To pull "five of this
reviewer's approvals" for a spot-audit, you would have to already know which checklists were that
reviewer's and which landed on Approve, with nothing that lists them. A pile of full records is hard to
count or sample from without reading all of it.

The log fixes that. It is one short, queryable row per handoff, and each row points back at the filed
checklist for that review. The checklist stays the full record of a single review. The log is the index
across all of them, and it points to each checklist rather than standing in for it.

## One row per handoff

A handoff is one build submitted for review (see `sops/hand-off-a-build-for-review.md`). One handoff is
one row.

The first review of that handoff sets the row. When the reviewer lands on a decision, you write the row:
the build, who reviewed it, the first-review outcome, and the date. Those first-review fields are now
fixed.

A send-back does not end there. The build gets fixed and comes back through the same handoff, and a
reviewer decides again. That re-review updates the same row's final outcome, an optional field described
below. It does not add a second row, and it does not change the first-review outcome already written. The
first-review outcome on the row is the first review's decision, and it stays that way for good, even after
the build is fixed and shipped.

This is the rule that keeps the send-back rate honest. The metric counts the first review only, so a build
that is sent back, fixed, and re-reviewed still counts once, as one send-back
(`analytics/metric-definitions.md`). If a re-review added a fresh row or overwrote the first outcome, a
rough build could come around the loop, get approved the second time, and quietly erase its own send-back.
One row per handoff, first-review outcome frozen, is what stops that.

## The fields

Five fields are required. They are the union of what the readers below need, and nothing more.

**Build.** The name or id of the build that was reviewed, for example a workflow name like
`intake-webhook-route-to-vendor`. It tells you which build a row is about, and it is how you find the
filled checklist filed with it. All build names in this repo are synthetic.

**Reviewer.** The person who ran the first review. This is the field the spot-audit named as missing
(`governance/review-spot-audit.md`), and it does two jobs. It lets the audit hand a build to someone who
did not review it, since you cannot steer a build away from its own reviewer without knowing who that was.
And it lets you see whether one reviewer's approvals keep coming back as audit misses, which is the pattern
the audit exists to catch. Use a role word or a made-up name, and keep it consistent so a reviewer's rows
group together.

**First-review outcome.** Exactly one of Approve, Approve with fixes, or Send back, the three outcomes the
reviewer SOP lands on (`sops/run-a-build-review.md`). This is the field the send-back rate counts, and it
never changes once written, per the rule above.

**Date.** The date of the first review. It is what lets you slice the log by period (this week, this month,
since the last audit) and read the cadence of reviews over time.

**Handed off.** The date the handoff packet was accepted and the build entered the queue
(`sops/hand-off-a-build-for-review.md`). Review latency is the first-review date minus this one, so without
it a wait cannot be computed at all. The queue row carries this date while a build waits, and that row
leaves the queue the moment the decision is logged, so the handoff time has to be copied here as the review
is written or it survives nowhere. Where a build was handed off with nothing else in flight and never got a
queue row, record it at handoff.

Those five are enough for the send-back rate, enough for the spot-audit to sample, and enough for review
latency to compute a wait. The next fields are optional. Name them now so the log has room to grow, and
leave them empty until something reads them.

**Final outcome (optional).** How the handoff ended after any re-reviews. A build sent back on the first
review, then fixed and approved, reads as "Send back" on its first-review outcome and "Approve" here. This
is the only field a re-review updates. It exists so a sent-back-then-shipped build is visible without
touching the first-review count, and it is optional because neither the send-back rate nor the audit needs
it. It is here for the day you want to read how a single handoff resolved.

**Audit fields (optional): audited, audit outcome, was it a miss.** Whether the handoff was later pulled
for a spot-audit, what the audit decided, and whether that differed from the original (a miss). The
spot-audit already produces these facts. A future review miss rate would read them, once that metric is
defined in `analytics/metric-definitions.md`. Until then, leave them out or leave them blank; the log has a
place for them so the metric has somewhere to read from when it arrives.

## How to keep it

- **Write the row when the first review lands.** The reviewer finishes `sops/run-a-build-review.md`, files
  the checklist, and adds one row here with the build, their name, the outcome, and the date. Same moment,
  one row. Later is when it gets skipped.
- **Keep it somewhere you can query.** A single sheet or a table, one row per handoff, with columns for the
  four required fields and space for the optional ones. The point of the log is that you can filter and
  count it, so keep it in a form that filters and counts by date, by outcome, and by reviewer.
- **One row per handoff, and not one per review.** A re-review finds the existing row and updates the final
  outcome. It does not add a second row for the same handoff. If you cannot tell a first review from a
  re-review, that ambiguity is the first thing to fix, because the readers of this log depend on that
  difference.
- **Point the row at the checklist.** The row is the index; the filled
  `governance/ai-build-review-checklist.md` is the full record. Keep a link, a file path, or a naming
  convention that gets you from the row to the checklist, so a count can always be opened back up into the
  reasons behind it.

## Who owns it

A log nobody is responsible for stops getting written, and the day it stops, both the metric and the audit
go blind. So the log needs a named owner, the same way section 8 of `standards/automation-standards.md`
treats every production build as having one accountable owner, with an explicit handover when the owner
changes.

Name one person who owns the review log. Their job is small: that a row gets written every time a review
lands, that there is one row per handoff and not two, that the log stays where the metric and the audit can
reach it, and that the format does not drift, so a row means the same thing in June as it does in December.
An unkept log is worse than none, because both the send-back rate and the spot-audit read it as if it were
complete. A missing row is a handoff the send-back rate never counted and a build the audit could never
sample. When the owner changes, hand the log over on purpose, the way the standard asks.

## What reads it

Four readers, each taking a different slice of the same row.

- **The send-back rate** (`analytics/metric-definitions.md`) reads the build, the first-review outcome, and
  the date. It counts, over a period, the share of handoffs whose first-review outcome was "Send back." It
  needs the three required fields the metric already names, and the frozen first-review outcome is what
  makes its count hold.
- **The spot-audit** (`governance/review-spot-audit.md`) reads those three plus the reviewer. It samples
  decided handoffs, weights the sample toward approvals, and uses the reviewer field to hand each build to
  someone who did not review it and to spot a reviewer whose approvals keep coming back as misses. The
  reviewer field is the one the audit was waiting on, and adding it here closes that prerequisite.
- **The review miss rate** (`analytics/metric-definitions.md`) reads the audit fields: audited, audit
  outcome, miss. It is the share of audited reviews whose decision the audit overturned, and it was written
  after this spec, so the audit fields named here are where it reads from. It needs both outcomes on an
  audited row, the frozen first-review outcome and the audit outcome, to tell a miss from a match and a
  false approval from an overturn the other way.
- **Review latency** (`analytics/metric-definitions.md`) reads the handoff date and the first-review date
  and takes the median of the gap between them, over the handoffs first-reviewed in a period. It is the
  reader that added the handoff field, since a wait cannot be computed from a row that records only when
  the review landed.

## What this does not settle

Be honest about the edges.

- **This defines the record, not the tool.** It says what a row is and which fields it carries. Whether
  that lives in a spreadsheet, a database table, or a Notion board is a choice left to whoever keeps it.
  Pick a form that filters and counts, and the rest is open.
- **The optional fields are optional for two different reasons now.** The audit fields have a reader: the
  review miss rate was written after this spec and reads them. They stay optional because only the rows a
  spot-audit pulled ever carry them, and most rows are never pulled. Final outcome still has no metric
  reading it, so it stays a convenience for anyone tracing what became of a build.
- **A returning build no longer settles itself here.** That question, whether a re-submission opens a
  second row or updates the first, is decided once in `governance/what-counts-as-one-handoff.md`, which
  defines a handoff as one trip through review and an arrival as each entry into the queue. This spec keeps
  one row per handoff, so a re-submission answering an open send-back updates only the optional final
  outcome on the existing row. A submission that is new work, or one that follows a handoff already closed
  by Approve or Approve with fixes, starts a new handoff and earns its own row. Read that file before
  writing a row for a build that has been here before.
- **A log only helps if reviews get logged.** The whole record rests on a row being written each time a
  review lands. A skipped row is invisible: the send-back rate counts a handoff that never entered the log
  as if it never happened, and the audit cannot sample a review it cannot see. The owner and the "write it
  when the review lands" rule exist for exactly this, and neither one forces the habit. The log makes an
  honest record possible. It does not make one automatic.

## What changed in v2

- Added a fifth required field, **Handed off**, the date the handoff packet was accepted. Review latency is
  the first-review date minus this one, and populating the log
  (`examples/a-populated-log-and-queue.md`) is what made the gap plain: the metric could be defined around a
  missing field and could not be read around one. This closes the prerequisite review latency named.
- Updated "What reads it" from three readers to four. The review miss rate is written now and reads the
  audit fields, so it is no longer described as future, and review latency joins as the reader that added
  the handoff field.
- Named a gap populating the log surfaced: the queue SOP and this spec describe a returning build two
  different ways, and neither file settles which reading wins.

## What changed in v3

- The returning-build question is settled, one day after v2 named it as open.
  `governance/what-counts-as-one-handoff.md` decides it: one row per handoff, where a handoff is one trip
  through review, and a re-submission answering an open send-back is a new arrival rather than a new row.
  This spec points there instead of flagging the gap.
- Named which submissions start a new row: new work, or anything following a handoff already closed by
  Approve or Approve with fixes.
- The **Handed off** field added in v2 is the handoff's first arrival, which is what keeps a row's wait
  fixed when the same build comes back.

---

*v3. A living spec. It defines the one record the send-back rate, the spot-audit, the review miss rate, and
review latency all draw on, reviewer and handoff fields included, and it now points at one ruling for what
counts as a handoff. The next pass gets tested by rows somebody else wrote.*
