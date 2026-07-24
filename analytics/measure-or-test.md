# Measure or Test (v1)

`sops/the-review-loop-in-order.md` shipped on Day 032, and it is built out of pointers: 22 distinct
file paths cited 26 times, and 24 inline version claims like "(v3)", every one of them a promise
about the current state of the tree. The index says in its own limits that it goes stale in a way
the pieces do not, that a wrong pointer is worse than none because an index is trusted, and that it
is the first thing to re-check when anything is added, renamed, or re-versioned. Nobody is checking
it.

Today's question was what a staleness check would actually read, whether a drifted pointer can be
caught more cheaply than a person re-reading the tree, and whether index staleness is a metric at
all. The answer is that this wants a check. It should not become a fifth entry in
`analytics/metric-definitions.md`, and this memo sits in `analytics/` to say why.

## The crux: decidable, not estimable

Every claim the index makes can be settled against the tree right now. A path exists or it does not.
A version claim equals the file's H1 version or it does not. The ground truth is sitting in the same
directory, unchanged, available to be read again as many times as you like.

That is what picks the tool.

- A **metric** summarizes past events whose truth cannot be re-derived. The run already happened, the
  review already landed, and all you have left is whatever the record kept. You reason about the
  number because the events themselves are gone.
- A **check** settles claims about a present state you can read directly. There is nothing to
  reconstruct and nothing to infer, so the output is a list of what is broken, or nothing.

Sampling is one way a metric copes, and only one of the four here actually samples. The other three
count every record they have, and their trouble is that the record can be missing rows: a run that
never fires is not in the run log, and a build never handed off is not in the review log. A
directory does not have that problem. Nothing is missing from a tree, because the tree is the thing
itself.

Estimating what you can simply know is strictly worse. It costs the same read and returns a
percentage in place of the two file names that failed. The rule worth carrying out of this: measure
what you must estimate, test what you can decide.

## What the check reads

Three rules, in words, so it could be implemented in anything.

1. **Every cited path resolves.** Pull every backticked token of the form `folder/file.md` out of the
   index, dedupe, and confirm each file exists. 26 citations, 22 distinct paths today.
2. **Every version claim matches, and so does the title beside it.** Each entry reads as a path, a
   title, and a version: "`sops/review-log-spec.md`, The Review Log (v3)". Every file the index cites
   writes its H1 as `# Title (vN)`, so the entry's title and version together must equal that H1 with
   the leading hash removed. 24 entries today, four of them a second citation of a path cited
   elsewhere, and the repeats get checked separately because they drift independently. Reading the
   title costs nothing extra, and it catches the pointer swapped to a different file that happens to
   share a version.
3. **Every in-scope file appears in the index.** Scope is a directory list rather than a category:
   every `.md` in `standards/`, `governance/`, `enablement/`, `sops/`, `analytics/`, `integration/`,
   and `examples/`, minus the index itself. `daily/`, `log/`, and the gitignored `private/` are out
   by folder. A file passes by being an entry or by being named in the "deliberately not here"
   section. This is the rule that earns its keep, because it catches the silent failure: a piece
   written and never indexed. Rules 1 and 2 walk only the claims the index already makes, so a file
   the index has never heard of passes both cleanly while the index goes quietly incomplete.

Rule 3 has one soft edge. The exclusion list is written by a person, so anyone can silence the rule
on any file by declaring it deliberately not here, and no program can tell a considered exclusion
from a lazy one. Rule 3 is mechanical given a scope somebody decided, rather than mechanical all the
way down.

Before this memo, the tally closed: 23 files across the seven folders, minus the index, equals the 22
it cites. That is a corroborating count and not the closure, since one phantom path and one
unindexed file cancel out to the same total. Rules 1 and 3 holding at the same time is the closure.
This memo is the twenty-fourth file, and it is the first thing rule 3 would flag, which is the rule
working on the day it was written. It either earns an entry under "Keep and measure" or gets named
as deliberately not here, and that call belongs to the same pass that adds the file.

There is also a fourth rule, found by writing this one. The index opens with "Seventeen review-side
pieces now sit across six folders, plus three weekly maps in a seventh, at versions from v1 to v4."
Four counts, all countable off the tree, all true today, and none of them read by rules 1 to 3. So
the opening tally becomes rule 4: recompute the four numbers and compare. The three rules looked
complete until somebody counted.

What the check deliberately does not read: the one-line description on each entry, and the ordering.
Both are below.

## Why a number is the wrong tool

Two versions of the metric are worth taking seriously.

The **snapshot rate** is the obvious one: index accuracy, correct claims over total claims, 46 in the
denominator today (22 distinct paths, plus 24 entry claims where the title and version are settled
against one H1 line). It is hand-computable from the records it draws on, which is the bar this
folder sets for adding a metric. It fails three ways.

**Its only acceptable value is 100 percent.** The dictionary sets no target for any of its four and
calls a zero send-back rate a warning sign rather than a goal, because a healthy review bounces
builds. There is no equivalent healthy amount of stale index. That holds independently of what the
index says about itself. A wrong pointer's whole cost lands on the one reader who follows it, and the
45 correct claims do nothing for that reader. A rate averages a cost that does not average, which is
why 96 percent tells you nothing about whether anybody was misled.

**The rate is a lossy summary of a result you already hold.** A proponent could sample, say ten
claims of 46, and skip the exhaustive read. The reason nobody would is that the per-claim cost is
opening a file and reading line one, so sampling saves a few seconds and buys back an estimate. Read
all 46, which is the only sane way to compute it, and you are already holding the failures by name.
Dividing throws that away.

**The trend is meaningless.** Every entry in the dictionary is read for its trend and says so. A
chart of pointer accuracy improving to 96 percent this month is not something anybody acts on. The
first drop is the whole event.

The **process metric** is the stronger candidate, and the snapshot version hides it: how often drift
gets introduced per period, or how long a wrong pointer survives before someone catches it. That one
is a fact about past events that are gone by the time you ask, it is not computable from a single
run, and its trend is worth reading, because three drifts last month says the write-time discipline
slipped. It fails for a different reason. It measures the check, so it cannot exist until the check
does, and it needs a run history this repo has not got, since one ad hoc run is not a series. Build
the check, run it for a while, and this becomes a real question. Today it is a metric with nothing to
count.

## Against the four metrics already here

Each of the four in `analytics/metric-definitions.md` stands in for something nobody can read
directly, and each carries a blind spot for that reason. The dictionary names all four itself.

- **Exception rate.** You cannot re-run last week's runs, so you count the log. A run that silently
  fails to trigger never lands there, so a falling rate can mean the work got cleaner or that fewer
  runs fired at all.
- **Send-back rate.** You cannot re-review a decided build to find out whether the call was right, so
  you count the outcome that was recorded. It cannot see the approval that should have bounced, which
  is why the next metric exists.
- **Review miss rate.** Sampling is the design, since auditing every review would move the trust
  problem up a level to whoever audits. It reads the rows that were pulled, weighted toward approvals
  on purpose, so it works as a detector and fails as an average.
- **Review latency.** You cannot know a wait that has not finished, so undecided builds contribute no
  duration, and a queue that clears its easy builds while the hard ones rot posts a fast median.

Four numbers, four blind spots, and the same cause under all of them: each stands in for something
nobody can read directly. The index check has no blind spot on the claims it reads, because what it
reads about is still sitting there to be read. Its blind spots are the claims nobody pointed it at,
which is a fact about the specification rather than the method, and rule 4 above is what finding one
looks like. Those four estimate. This one decides what it reads.

## What the check cannot catch

Semantic drift, and this is the real limit. Each of the 24 entries carries a line saying what the
file is for and when to open it. A path can resolve and a version can match while that line has
quietly stopped being true of the file it points at, and the re-version that made it untrue is
exactly the event rule 2 reports as fine. A reader who follows a correct pointer into a file that no
longer does what the line promised has been misled by an index that passed its check. The check
compares a path and a string, and meaning is neither of those.

Ordering is the same problem one level up. The index orders the pieces by when you need them: learn
the loop, do your part, keep and measure, see it run. If the shape of the loop changes, a stage added
or two merged, that order can be wrong while every mechanical claim stays green.

So the split is clean: mechanical claims to the check, meaning claims to a person. A person re-reads
the descriptions and the order on a cadence, and the check keeps that reading from being spent on
broken pointers.

## When to run it

At the moment of the change that would break it. The index already names the trigger in its own
limits, so a check that runs then costs nothing beyond what the index already asks for, and the
person running it has the change in front of them.

This is the principle behind the write-time check in `enablement/keeping-the-review-log.md`, whose
four steps sit in front of the person before the row is written, because that is the only moment the
answer is cheap. The person renaming a file knows which pointers they touched. An audit three weeks
later tells you a pointer was wrong for three weeks, and by then someone has followed it. The
cheapest place to protect an invariant is the moment it is created.

## The honest state

This exact check was run once, by hand and ad hoc, when the index shipped on Day 032. All 22 paths
resolved and all 24 version claims matched their file's H1. Zero mismatches.

That single run is also the only cost datapoint there is. One pass by hand across 22 files is the
measured price, and one command is an estimate for a program nobody has written. Cheapness is the
premise this whole argument rests on, since a check only beats a metric when the exhaustive read is
genuinely cheap, so it is worth saying which half of that price was actually paid.

Running something once is not a habit. This repo has shipped no code, so what exists here is a
specification, and nothing runs it, and a specified check nobody runs catches exactly as much as no
check at all. That is the same shape as the log nobody keeps (`sops/review-log-spec.md`) and the
audit nobody performs. Writing down what to read was the cheap half.

---

*v1. A living memo. The next pass records what the first real drift turned out to be, whether rule 3
caught a file nobody indexed, and whether the check ever became something a machine runs.*
