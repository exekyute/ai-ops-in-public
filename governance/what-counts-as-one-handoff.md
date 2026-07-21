# What Counts as One Handoff (v1)

Writing real rows into the review log for the first time (`examples/a-populated-log-and-queue.md`) turned
up a conflict no document in this repo settles. `sops/run-the-review-queue.md` calls a re-submission a
fresh handoff that re-enters at the back of the queue at a new handoff time, while
`sops/review-log-spec.md` keeps one row per handoff, freezes the first-review outcome, and says a
re-review does not add a second row. Each file is right about the record it governs, and the two readings
collide the moment someone has to write the row, so the same event can be recorded two ways by two honest
people. What rides on the answer is the send-back rate: read one way, a build that bounces and is then
approved earns a second row and waters down its own send-back. This file decides it once, and both of
those files are being updated separately to point here.

## The root cause: one word doing two jobs

The disagreement is a terminology collision. The word "handoff" is doing two jobs in this repo, and both
are fair readings of `sops/hand-off-a-build-for-review.md`, which describes a loop where a sent-back build
re-enters at step 1, rebuilds its packet, and hands off again at step 3, so every trip crosses the same
handoff point.

The queue took the event reading. Each time a build is handed over, something arrives that has to be
ordered and assigned. That reading fits a queue, because a queue orders what is waiting right now, and a
build that comes back after a send-back is genuinely a new thing waiting, with its own age and its own
place in line.

The log and all three review-side metrics took the episode reading. One row, one first review, one frozen
outcome, one wait, one audit slot. The send-back rate counts those rows, the review miss rate reads audit
fields on those rows, and review latency takes one duration per row. That reading fits a log, because the
log is the permanent count, and each trip through review should land in it once.

Each reading is correct for the record that uses it. Both records need a unit, the units are different
things, and giving them one name is what produced the conflict. The fix is two names.

## The two definitions

**A handoff** is one build's trip through review, from the first time it is handed over to the decision
that closes it. The review log keeps one row per handoff (`sops/review-log-spec.md`). It is the unit all
three review-side metrics count: the send-back rate, the review miss rate, and review latency
(`analytics/metric-definitions.md`).

**An arrival** is each time a build enters the queue waiting on a decision, including a re-submission
answering a send-back. The review queue keeps one row per arrival and orders arrivals oldest first by
default (`sops/run-the-review-queue.md`), with the small priority lane that SOP already keeps, which this
ruling does not touch.

So one handoff can have more than one arrival: the first submission, plus any re-submission that answers a
send-back. Where the queue SOP calls a returning build a fresh handoff, it now says a fresh arrival, which
is the wording it already reaches for one clause later. The rest of that ordering rule is unchanged apart
from that one word. A re-submission still enters at the back at its new arrival time and takes its turn
like any other waiting build.

While a re-submission waits, its build holds a frozen log row and a live queue row at the same time. That
is the state the queue SOP already describes, now with a name for each half.

## The test: what is the submission answering

When a build shows up for review, ask what the submission is answering.

- **It answers the reasons on an open send-back.** Same handoff. Same log row, first-review outcome still
  frozen, final outcome updated when the re-review lands, and a new arrival in the queue at its new
  arrival time, at the back of the line.
- **It is new work, or the handoff before it is already closed.** New handoff. New log row, its own first
  review, its own frozen first-review outcome, and its own first arrival. A handoff is closed when its
  review landed on either passing outcome, Approve or Approve with fixes (`sops/run-a-build-review.md`), or
  when the build was abandoned. Approve with fixes closes it even while the small listed fixes are
  outstanding, because the path ends there (`sops/hand-off-a-build-for-review.md`). An unanswered send-back
  is the one outcome that leaves a handoff open.
- **The practical version:** an open send-back is what keeps a handoff open. Close it and the next
  submission starts a fresh one.

Day 029's log has both cases sitting three rows apart, which is how the question surfaced. Row 4,
`signup-webhook-to-crm`, was sent back on Jul 4, and the re-submission in that file's queue snapshot
answers the reasons on that open send-back: one handoff with two arrivals, one log row frozen at Send
back, one queue row three days old on the Jul 20 read. Row 1, `invoice-reminder-sheet-to-slack`, is the
other side of the test. Its earlier trip around the loop closed with an approve-with-fixes
(`examples/a-build-through-the-loop.md`), and it came back later with a new change: closed predecessor,
new work, so a new row carrying its own first review. Before this ruling, the only thing separating those
two rows was the judgment of whoever happened to write them.

## Why this reading wins

The alternative is that a re-submission opens a new log row. That hands back the exact gaming the frozen
first-review outcome was built to stop.

Follow it through. A build is sent back, fixed, and approved on the second trip. Under the new-row reading
it produces a Send back row and an Approve row, two entries in the denominator and one in the numerator,
so its own rework improves the send-back rate. The rougher the build, the more trips it takes, and the
more passing rows it contributes. A build that bounced would dilute the very number that exists to count
bounces.

`analytics/metric-definitions.md` already rules this out in the send-back rate's "What counts": a build
that is sent back, fixed, and re-reviewed "still counts once here, as one send-back, so a rough build
cannot quietly improve the rate by coming around the loop again." The metrics were written on the episode
reading from the start, and the queue's ordering rule is the only place that disagreed about what the log
should count. The word itself slipped in one more place, the field names both records carry, and the
section below settles those too.

Two consequences fall out of the same point. Freezing the first-review outcome means nothing if a build
can simply open a fresh row, since the frozen field is then trivially routed around. And the send-back
rate only reads as the share of builds that bounced when each trip through review counts once in the
denominator; let one trip contribute two rows and the denominator becomes a count of submissions, which is
a different number wearing the same name.

## What this costs

Choosing the review-episode reading buys metric integrity and costs latency completeness. Say that trade
out loud instead of presenting the ruling as free.

Review latency is a median over first reviews, one duration per log row
(`analytics/metric-definitions.md`). A re-submission is a new arrival, so it waits again, and that second
wait attaches to no log row: the row is frozen, and the only field a re-review updates is the optional
final outcome, which carries no date. A build that is sent back and re-reviewed can wait weeks in total
and show only its first wait in the median. Day 029 makes the cost concrete. Row 4's 2-day duration is the
only one it will ever contribute, while its re-submission had sat 3 more days by the Jul 20 read with
nowhere to record them.

That is a real blind spot, and it is a deliberate trade. Review latency's "What counts" already names it,
and this ruling is what makes it permanent.

What still sees it is the queue. Under this ruling every arrival gets its own row carrying its own arrival
time, so a re-submission is visible on the live queue from the day it starts sitting, and it enters the
oldest-waiting age once it becomes the longest-waiting build. Day 029 shows both halves: the re-submission
is on the board at 3 days while the oldest-waiting age reads 19 days off `quarterly-access-review`. The
median is the lagging number about builds that are done waiting. The queue moves while a build is still
waiting, and that is what makes this trade survivable. Read the two together, the way the latency entry
already asks.

## What each record does now

- **The review log keeps one row per handoff** (`sops/review-log-spec.md`). One trip through review,
  first-review outcome frozen, the optional final outcome recording how the trip ended, one duration per
  row. A re-submission answering an open send-back updates only that optional final outcome. Build,
  reviewer, first-review outcome, date, and **Handed off** all stay as first written, so the row keeps its
  original wait. The **Handed off** field is the handoff's first arrival, which is why review latency is a
  first-review wait and why a re-submission's later arrival time never overwrites it.
- **The queue keeps one row per arrival** (`sops/run-the-review-queue.md`). Every wait has a row while it
  is waiting, first submissions and re-submissions alike, ordered oldest arrival first. Each row carries
  its own arrival time, so a re-submission's queue row shows the re-submission date while its log row
  still shows the first. The row leaves when a decision is logged.
- **A build under re-review sits on both lists at once.** One frozen log row, one live queue row. That
  state is normal now, with a word for each side of it.

`analytics/metric-definitions.md` needs no change for this. Its "handoff time" appears in two formulas and
means an arrival in both: review latency subtracts the log's **Handed off** field, which is the first
arrival, and the oldest-waiting age reads a queue row, which is whichever arrival is sitting there. Both
still compute what they say. That term is the one place the old word survives, so a reader should know
which arrival it points at in each formula.

Both SOPs point here for the definitions and the test, so the counting rule lives in one place and neither
file restates it in its own words. The queue SOP trades "fresh handoff" for "fresh arrival" in the same
pass. When a later file needs one of these words, this is where it is defined.

## What this does not settle

Be honest about the edges.

- **It settles the counting question and forces nobody to record it correctly.** Two people can now reach
  the same answer from the same event, which is the whole point. Neither this file nor the two it updates
  makes anyone ask the question before writing a row, and someone who opens a new row out of habit
  produces the same bad data this ruling exists to prevent. The log's named owner and the
  write-it-when-the-review-lands rule (`sops/review-log-spec.md`) are what stand behind it. An owner is a
  person, and a person is not a control.
- **The test has a fuzzy edge, and it picks a side anyway.** A builder who fixes the send-back reasons and
  ships unrelated new work in the same submission is answering an open send-back, so the test calls it one
  handoff. That reading is defensible and it can be wrong at the margin, where most of the new content is
  new. The alternative, splitting one submission into two handoffs, reopens the gap this file closes.
- **"Abandoned" has no moment attached to it.** A handoff closes on a passing outcome or on abandonment,
  and nothing in this repo declares an abandonment. On paper, a send-back nobody ever answers keeps its
  handoff open forever, so a submission months later reads as the same handoff by the letter of the test.
  Use judgment there, and if that case shows up for real, it wants a rule of its own.
- **The latency trade is deliberate and it is still a loss.** Total time in review, first arrival to
  close, is a number this repo cannot compute from its own records, and no metric here asks for it yet.
  The fix on the day it bites is a record that carries arrivals with their own dates, because the moment a
  re-submission earns its own log row the send-back rate loses its meaning again.
- **This was decided against authored rows.** The conflict surfaced in synthetic rows written by the same
  person who wrote the specs, and it is being settled against those same rows. This ruling has met exactly
  one case, the one Day 029 wrote down. A real queue is where a returning build the test cannot classify
  would finally show up.

---

*v1. A living ruling. It splits one overloaded word in two, so the log counts trips and the queue counts
waits. The next pass revisits it when a real queue produces a returning build the test cannot place.*
