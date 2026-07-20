# A Populated Log and Queue (v1)

Every metric in this repo has been a formula with nothing under it. `analytics/metric-definitions.md`
gives the send-back rate, the review miss rate, and review latency each a formula, a list of what
counts, and a worked example assembled out of figures invented for the paragraph.
`sops/review-log-spec.md` and `sops/run-the-review-queue.md` define the two records those formulas read
from, and both have been empty shapes waiting on rows. This file fills them: a review log of twelve
handoffs, a queue snapshot of four builds still waiting, and the three review-side metrics read off
those rows rather than restated as definitions. Everything here is synthetic and authored by one person
to exercise the definitions, with role labels (Reviewer A, Builder X) and never real people, companies,
or vendors.

The period is the first three weeks of July. The log holds the twelve handoffs whose first review was
logged in that window. The queue was read on Jul 20 and holds what was still waiting at that moment.
Every number below is hand-checkable against the tables, which is the rule
`analytics/metric-definitions.md` sets for a metric belonging in it at all.

## The review log

One row per handoff, per `sops/review-log-spec.md`. The first-review outcome is frozen on the row and
never rewritten. The audit fields are filled only on the rows a spot-audit pulled
(`governance/review-spot-audit.md`) and blank on the rest.

| # | Build | Reviewer | Handed off | First review | Wait (days) | First-review outcome | Audited | Audit outcome | Miss |
|---|---|---|---|---|---|---|---|---|---|
| 1 | invoice-reminder-sheet-to-slack | Reviewer A | Jun 30 | Jul 1 | 1 | Approve with fixes | yes | Approve with fixes | no |
| 2 | feedback-form-to-crm | Reviewer B | Jun 30 | Jul 1 | 1 | Approve | yes | Send back | yes |
| 3 | weekly-report-drive-to-email | Reviewer A | Jul 1 | Jul 3 | 2 | Approve | yes | Approve | no |
| 4 | signup-webhook-to-crm | Reviewer C | Jul 2 | Jul 4 | 2 | Send back | no | (not audited) | (n/a) |
| 5 | ticket-escalation-slack-alert | Reviewer B | Jul 3 | Jul 6 | 3 | Approve | no | (not audited) | (n/a) |
| 6 | inventory-sync-sheet-to-db | Reviewer C | Jul 4 | Jul 7 | 3 | Approve with fixes | yes | Approve with fixes | no |
| 7 | expense-approval-router | Reviewer A | Jul 6 | Jul 10 | 4 | Approve | no | (not audited) | (n/a) |
| 8 | nps-survey-dispatch | Reviewer B | Jul 7 | Jul 12 | 5 | Send back | yes | Send back | no |
| 9 | contract-renewal-reminder | Reviewer C | Jul 8 | Jul 14 | 6 | Approve | no | (not audited) | (n/a) |
| 10 | lead-dedupe-nightly | Reviewer A | Jul 9 | Jul 17 | 8 | Approve with fixes | no | (not audited) | (n/a) |
| 11 | payroll-file-drop-check | Reviewer B | Jul 10 | Jul 19 | 9 | Approve | no | (not audited) | (n/a) |
| 12 | vendor-onboarding-checklist | Reviewer C | Jul 5 | Jul 19 | 14 | Send back | no | (not audited) | (n/a) |

Three rows carry history from builds this repo has already walked end to end, and they need naming
before the arithmetic.

**Row 1, `invoice-reminder-sheet-to-slack`,** is Day 015's build
(`examples/a-build-through-the-loop.md`). That trace ran one handoff around the loop twice: sent back on
the first review for the double-post, then approved with fixes when the fixed build came back. Both
trips belong to that single handoff, so under `sops/review-log-spec.md` they share one row, first-review
outcome frozen at Send back, dated before this window and sitting outside this log. The row above is a
later handoff of the same build, a new change handed off fresh on Jun 30. Its Approve with fixes is that
handoff's own first review and its 1-day wait is a first wait, which is why it belongs in the population
below. The audit landed where the review landed, so the row is a match.

**Row 2, `feedback-form-to-crm`,** is Day 022's build (`examples/a-rubber-stamped-approval.md`): the CRM
token typed into the HTTP Request node's authorization header, marked fine by the builder without
opening the node, marked fine again by the reviewer, approved, then caught when the spot-audit opened
the node. Its row is the one place in this log where the first-review outcome and the audit outcome
disagree, and it is why the miss rate below is above zero.

**Row 4, `signup-webhook-to-crm`,** was sent back on Jul 4, and its re-submission is sitting in the queue
below. Here the two records pull against each other. `sops/run-the-review-queue.md` calls a
re-submission a fresh handoff and puts it at the back of the queue at its new handoff time.
`sops/review-log-spec.md` keeps one row per handoff, freezes the first-review outcome, and gives a
re-review only the optional final-outcome field, which carries no date. Read the first way, the build
has a second handoff and should produce a second row and a second duration. Read the second way, it has
one row that can never gain a date from a re-review. This file takes the log spec's reading, which is
the one the queue SOP itself points at when it says the log keeps the original row and only the queue
place is new. So row 4 stays frozen at Send back with its Jul 4 date, its 2-day duration is the only one
it will ever contribute, and the second wait the re-submission is accruing appears nowhere in the
latency median. Writing row 1 is what made the question visible: the same build coming back with new
work gets its own row, the same build coming back after a send-back does not, and no single document
says how to tell those two apart.

`sops/review-log-spec.md` requires four fields, the build, the reviewer, the first-review outcome, and
the date, and it names the audit fields as optional, which is what fills the last three columns here. Of
the rest, the row number is a reading aid and "Wait (days)" is derived from the two dates beside it
rather than stored. "Handed off" is the one real field the spec does not have, latency cannot be
computed without it, and the closing section deals with what that means for the spec.

## The queue snapshot

Read Jul 20. Four builds handed off and still waiting on a decision, ordered oldest first per
`sops/run-the-review-queue.md`.

| Build | Builder | Handed off | Waiting (days) |
|---|---|---|---|
| quarterly-access-review | Builder X | Jul 1 | 19 |
| crm-field-normalizer | Builder Z | Jul 6 | 14 |
| backup-freshness-check | Builder Y | Jul 11 | 9 |
| signup-webhook-to-crm (re-submission) | Builder X | Jul 17 | 3 |

The snapshot carries three of the five fields the queue SOP puts on a waiting row: the build, who built
it, and when it was handed off. Lane and assignee are left off because nothing read below uses them, and
"Waiting (days)" is derived from the handoff date and the Jul 20 read rather than stored. No row is in
the priority lane, so the median below is not mixing a fast lane with a slow default line, which is one
of the ways the latency entry says a pooled median can end up describing neither group.

The bottom row is row 4 of the log coming back around. The queue SOP sends a re-submission to the back
as a fresh arrival at its new handoff time, so it has been waiting 3 days as of Jul 20 while holding a
frozen log row from Jul 4. It is the state the queue SOP describes, one build on both lists at once, and
the queue is the only record that sees the second wait.

Three of these four rows have never been decided, so they have no first-review date to subtract from and
produce no duration at all. The fourth is out of the median for a different reason: its log row was
decided on Jul 4, that row's 2-day duration is already counted, and the median takes one duration per
log row, so the wait it is accruing now adds nothing. Either way, no row in this table moves the median,
which is exactly why the latency entry asks for the oldest-waiting age beside it.

## The three readings

Each one is computed off the tables above, and each one can be checked by hand.

### Send-back rate

    send-back rate = first-review send-backs / handoffs reviewed

Twelve handoffs got a first review in the period, so the denominator is 12. Three of those first reviews
landed on Send back: row 4 (`signup-webhook-to-crm`), row 8 (`nps-survey-dispatch`), and row 12
(`vendor-onboarding-checklist`).

**3 / 12 = 25 percent, on a count of 12.** The complement, first-pass approval rate, is 9 / 12 = 75
percent, and the two sum to 100 percent.

The metric asks for the split rather than the bare rate, because "Approve with fixes" is a soft pass.
Counting down the outcome column: 6 clean Approves (rows 2, 3, 5, 7, 9, 11), 3 Approve with fixes (rows
1, 6, 10), 3 Send backs (rows 4, 8, 12). So the 75 percent that passed is 6 clean and 3 carrying a fix
list.

### Review latency

    review latency = median(first-review date minus handoff time) over handoffs first-reviewed in the period

Twelve durations, one per log row, taken from the Wait column. Sorted:

    1, 1, 2, 2, 3, 3, 4, 5, 6, 8, 9, 14

Twelve is an even count, so the median is the average of the 6th and 7th values. The 6th is 3 and the
7th is 4.

**(3 + 4) / 2 = 3.5 days, on a count of 12 first reviews.**

The companion is the oldest-waiting age, read off the live queue rather than the log:
`quarterly-access-review`, handed off Jul 1, read Jul 20, **19 days, with 4 builds still waiting.**

### Review miss rate

    review miss rate = overturned audited reviews / reviews audited

Five rows carry audit fields, so the denominator is 5: rows 1, 2, 3, 6, and 8. The draw is weighted
toward approvals the way `governance/review-spot-audit.md` requires, four approvals (rows 1, 2, 3, 6)
and one send-back (row 8). On four of those five the audit landed where the original review landed. Row
2 broke the pattern. The original review said Approve and the audit said Send back.

**1 / 5 = 20 percent, on 5 reviews audited.**

That single overturn is a false approval, the subset the metric pulls out as the one the send-back rate
cannot see by construction. So the false-approval count is 1 of 5 audited, and it is the outcome Day
022's example predicted before there were any rows to show it in.

The metric also asks for a slice by reviewer before the pooled number is read. Reviewer B had two rows
audited (2 and 8) and one of them was overturned. That is a fact about two rows. Two audited reviews
cannot separate a reviewer with a habit from a reviewer who had one bad day, and reading it as either
would be inventing a pattern out of a single data point.

## What the numbers say together

Read one at a time, two of these three look like an ordinary queue in a decent month. A 25 percent
send-back rate sits exactly where the metric's own worked example sits, with a 75 percent first-pass
approval rate behind it. A 3.5-day median wait describes a queue turning builds around inside a week.
Neither number, read alone, asks for anything.

The latency median is silent on the four builds still waiting, one of them 19 days old. It describes the
twelve that finished. This is the survivorship trap the latency entry names, showing up in rows rather
than in a caution paragraph: the twelve that got decided are partly the twelve that were easy to decide,
and the median looks fast partly because the slow builds have not been decided yet. Nineteen days is
more than five times the median and contributes nothing to it. The oldest-waiting age is the only one of
these readings that can see it.

The miss rate says something the send-back rate structurally cannot. One of five audited reviews was
overturned, and that one is a false approval: a build that passed its first review and would not have
passed an honest second look. It sits inside the 75 percent first-pass rate as if it were clean prep.
The send-back rate did what it is defined to do, counting first-review outcomes, and this build's
first-review outcome was Approve.

Put together: two of the three numbers read healthy and the queue is not. There is a build 19 days old
that nobody has decided, and there is an approval inside the passing column that a cold re-review
reversed. No single number here would have said so. The send-back rate cannot see the false approval,
the latency median cannot see the 19-day build, and the miss rate says nothing about waiting at all.
Reading them one at a time produces a clean report. Reading them as a set produces the two problems, and
this is the first time in this repo that can be shown with rows instead of asserted.

## What this closes and what it does not

**What it closes.** The three review-side metrics now have records to compute from, and computing them
exercised the definitions end to end: one row per handoff, first-review outcome frozen, a re-submission
that appears in the queue and stays out of the median, audit fields filled only on audited rows, a
median over an even count, and a false approval separable from the pooled overturn count. The
definitions held together under an actual read, and every reading came out hand-checkable from the
tables, which is this repo's own bar for whether a metric is defined well enough to exist.

**What it does not close.** These rows are authored. One person wrote twelve log rows, five audit
results, and four waiting builds to exercise definitions that same person wrote. There is no real team
here, no real reviewer pool, no real builder, no real audit, and no real queue that filled up on its own
while people were busy. Nothing here was observed. What this shows is that the metrics compute and the
definitions are coherent with each other, and it shows nothing whatsoever about a real queue. The
recurring gap every weekly map since week 2 has named, that this is all specs and synthetic data, is
narrower after this file and still open. Most of the awkward cases in this log are ones the specs
already anticipated, which is what you get when the same person writes the specs and then writes rows to
exercise them. One case was not anticipated, and it is named at the bottom of this section. Real rows
produce that kind at a rate one author cannot fake, and those are the cases that would actually test the
definitions.

**The samples are tiny, and each metric's own volume warning applies to its own reading here rather than
to some hypothetical read.**

- The send-back rate is 3 over 12. The entry warns that a 25 percent rate on a small count is one
  ordinary week rather than a trend, and 12 is a small count. One row flipping from pass to send-back
  takes it to 4 / 12, or 33 percent.
- The latency median is over 12 durations, and the entry says to write the count next to it every time
  for exactly this reason. It also sits between two adjacent values, so a single extra row lands on one
  side or the other and moves it.
- The miss rate is 1 over 5. One more overturn takes it to 40 percent, and one more audited review that
  matched takes it to 1 / 6, about 17 percent. Reading it as "one in five reviews is wrong" would
  overstate it badly. One overturn is a record, and there is no second cycle to compare it against.
- The per-reviewer slice is thinner still, at two audited rows for the reviewer who owns the miss.

**Two structural blind spots survive intact.** The miss rate reads only the five rows that were audited,
so a bad approval can be sitting in the seven that were not pulled, and this file would look identical
if it were. And the audit sample is weighted toward approvals on purpose, which makes the 20 percent a
detector aimed where misses hide rather than an estimate of the true miss rate across all twelve
reviews. Both are the shape of the instrument, and neither goes away when the rows get real.

**Populating the record forced two gaps into the open.** The first was already on the list. The latency
entry named a prerequisite: the handoff time does not survive onto the log row, and the four required
fields in `sops/review-log-spec.md` are the build, the reviewer, the first-review outcome, and the date,
with no handoff time among them. The log above carries a "Handed off" column because a wait cannot be
computed without it. The metric could be defined around a missing field and could not be read around
one, and trying to subtract two dates from four columns that carry one makes the gap obvious in a way
that reading the definition does not. That field belongs in the spec's required list, and the spec is
being bumped separately to add it. The second gap was on nobody's list: the re-submission question in
row 4, where the queue SOP calls a returning build a fresh handoff and the log spec keeps it as one
frozen row, and the two readings disagree the moment you try to write the row. This file picked one and
said which. The specs should say it in one place, and they do not yet. That gap took one attempt at
writing real rows to surface, which is a small piece of evidence for what the rest of the rows would do.

---

*v1. A living example. It is the first record in this repo with rows instead of formulas, and it turns
three definitions into three readings a reader can check by hand. The next pass replaces authored rows
with rows produced by an actual run of the loop, where the cases the specs did not anticipate can
finally show up on their own.*
