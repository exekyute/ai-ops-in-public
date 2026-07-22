# Keeping the Review Log (v1)

You keep the review log. Most of the time that is the simplest job in this repo: a build shows up for its first review, you write a new row, and you are done. The ruling in `governance/what-counts-as-one-handoff.md` settled what a handoff is, so two people reading the same event reach the same answer, but a ruling does not write rows, and someone who opens a new row out of habit produces the exact bad data that ruling exists to prevent. The log still rests on the person holding the pen. This guide is the write-time habit for the one case that is not simple: a build that has been in the log before.

## Why only the returning build carries the risk

A first-time build cannot be recorded wrong in the way that matters. You have never seen it, so a new row is the only row it could get, and there is nothing to get wrong. The whole risk lives in the returning build, and inside that, in one reflex: opening a new row for a build whose last row you should have updated instead.

Follow what that one wrong row does. A build is sent back on its first review, so its row is frozen at Send back (`sops/review-log-spec.md`). The builder fixes it and hands it back, and it passes. If you open a fresh row for that passing re-review, the build now sits in the log twice, one Send back and one Approve, and its own rework has just earned it a passing row. The send-back rate is first-review send-backs over handoffs reviewed (`analytics/metric-definitions.md`), so a build that bounced has watered down the number that exists to count bounces. The rougher the build, the more trips it takes, and the more passing rows it collects. That is the exact gaming the frozen first-review outcome was built to stop, and it gets in through the pen rather than through the spec. Every other row in the log is safe from it. This one is the whole job.

## Before you write the row

Run this before you write any row. It is four steps, and almost every build stops at the first.

1. **Has this build been in the log before?** Search the log for its name. If no, write a new row and you are done. This is nearly every row.
2. **If yes, find its most recent row and check for an open send-back.** An open send-back is a first-review outcome of Send back with no passing outcome recorded after it. An open send-back is what keeps a handoff open (`governance/what-counts-as-one-handoff.md`).
3. **If there is an open send-back and this submission answers its reasons, it is the same handoff.** Do not open a new row. Update the existing row's optional final outcome when the re-review lands, and add a new arrival to the queue at its own arrival time (`sops/run-the-review-queue.md`). The first-review outcome and its date stay frozen where they are.
4. **Otherwise it is a new handoff, so write a new row.** That covers a last row that closed on Approve or Approve with fixes, a build that was abandoned, and a submission that is new work rather than an answer to the send-back reasons. The new row gets its own first review and its own frozen first-review outcome. An open send-back is what holds a handoff open; close it and the next submission starts a new one.

## When you are unsure

Some returning builds will not sort cleanly. The builder fixes the send-back reasons and ships some unrelated new work in the same submission, or the row does not make clear whether the last outcome closed the handoff. When you cannot tell whether it is the same handoff or a new one, treat it as the same handoff: update the existing row, and do not open a new row.

The default leans that way on purpose, because it picks the smaller error. Merge a row that should have been split and you understate activity by one row: a build that should have shown two handoffs shows one, and no metric's meaning changes. Split a row that should have been merged and you hand a bounced build a fresh passing row, the same dilution the section above traces, the failure the whole ruling exists to prevent. One error is a quiet undercount. The other is the gaming itself. When you cannot tell which is right, take the undercount.

## Signs you are about to slip

Two tells, both of which land before the row is written, which is the only moment you can catch them.

- **You are reaching for a new row for a build name you have seen recently.** Stop and open its last row. A name you recognize is the signal that step 1 might not be a no, so check it for an open send-back before you write.
- **The build in front of you is a fix for a send-back you remember writing.** That memory is the answer: a fix for an open send-back is an update to that frozen row plus a new arrival in the queue, and a new row is the wrong move.

Day 029's log has this exact case sitting in it (`examples/a-populated-log-and-queue.md`). Row 4, `signup-webhook-to-crm`, was sent back on Jul 4 and frozen there, and its re-submission is in that file's queue snapshot answering the send-back reasons: one handoff, two arrivals. The log row stays frozen at Send back with its Jul 4 date, and the queue carries the re-submission at its own arrival time, three days old on the Jul 20 read. Three rows up, row 1, `invoice-reminder-sheet-to-slack`, is the other side of the test. An earlier trip closed on Approve with fixes, and the build came back later with a new change, so it earned its own new row. Same log, both cases, and before the ruling the only thing telling them apart was the judgment of whoever wrote them.

## What this cannot do

Be honest about the edges.

- **A guide makes the right call easy and does not force it.** It puts the question in front of you at the moment you write the row, and it still rests on you stopping to ask. Someone who opens a new row out of habit without asking produces the same bad data anyway. This is the same limit the ruling names about itself (`governance/what-counts-as-one-handoff.md`): the check only works if you run it.
- **The log still rests on its named owner.** `sops/review-log-spec.md` gives the log one accountable person whose job is that a row gets written each time a review lands, one row per handoff and not two, and the format does not drift. This guide is a tool for that person and for anyone writing rows under them. It does not replace the owner. An owner is a person, and a person is not a control.
- **This only helps a log that is actually kept.** A row that never gets written is invisible to every reader downstream: the send-back rate never counts the handoff, and the audit can never sample it. The write-time check has nothing to run on a review that was decided and never logged. It sharpens the rows you do write, and it cannot conjure the ones you skip. Getting the returning-build case right matters only once the ordinary rows are all there.

---

*v1. A living guide. It turns one ruling into a single write-time check, so the handoff test gets applied when the row is written instead of argued after. The next pass folds in the first returning build a real queue produces that this check cannot cleanly place, and tightens any step a wrongly-split row showed was too easy to skip.*
