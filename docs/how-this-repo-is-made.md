# How This Repo Is Made (v1)

This repo has shipped one artifact a day since 2026-06-22, on a fixed pillar rotation, and it stops at Day 049: something over eighty thousand words in seven weeks. Nearly every sentence was drafted by a model. I pick every subject, write every brief, check claims against the files on disk, and decide what ships. This note was made the same way, and you should weigh it on those terms.

Two reasons. At this volume the question occurs to anybody reading carefully, and an unanswered one gets answered by the reader, usually worse than the truth. And this repo argues, across two files on how to review honestly, [the inspection guardrail](../governance/inspection-required-checks.md) and [the rubber-stamp guide](../enablement/reviewing-without-rubber-stamping.md), that a mark made off evidence that does not answer the question is a rubber stamp. [The spot-audit guardrail](../governance/review-spot-audit.md), the control that re-reviews the reviewer, adds that a control checking one party and not the checker moves trust up a level instead of removing it. Staying quiet about how this text is produced would commit the error the repo warns about.

## How a day gets made

**The subject.** The pillar rotation on [the front page](../README.md), the entry point listing the pillars and the ground rules, fixes what kind of artifact the day owes. The rest comes from what the day before left open: every daily entry ends on a Next section naming a limit the day hit. The brief starts there. I write it myself, including the argument I think is right, which is the part most often wrong.

**Two drafts, merged.** Two drafts get generated from different angles against that brief, by the same model family, then merged into a first draft.

**The attacks.** That draft goes to several adversarial passes, each with one job, none seeing the others' findings. One enforces the voice rules, which live in a written standard the repo keeps private. One fact-checks every claim against the files on disk. One attacks the argument. One asks whether a person could act on the result. Findings come back as a list, and a finalizer, another automated pass, applies the correct ones.

**The decision.** I read the draft and the whole findings list, including what the finalizer rejected, check claims against the tree, cut what is over-claimed, and rewrite by hand when the prose has gone bloodless. Nothing ships that I have not read. None of that leaves a record: no log of which findings were applied, which I overruled, or which passages I rewrote. That is where this process falls short of the bar the rest of the repo sets, since [the log spec](../sops/review-log-spec.md) pins one row per handoff because a decision nobody wrote down is indistinguishable from one nobody made.

## What the checking has caught

"It gets checked" is worth nothing unless the checking has caught things. It has, some from an attack pass, some from drawing the thing or rereading it before it shipped. Half of each catch below is checkable: the shipped claim differs from the one I brought, and both the dated entry and the file are open. That a pass produced the change is my word alone.

[Day 039](../daily/day-039.md) shipped [the change-control standard](../standards/prompt-and-model-change-control.md), which puts a prompt and a model version under one procedure. The first draft claimed change control has no vocabulary for a change with no changer. That came back refuted: lockfiles, version ranges, and operating systems that patch themselves all answer changes nobody made. The shipped claim is narrower and true: the mechanism is old, and what is new is that a model moving under you returns prose that still parses, still validates, and finishes green.

[Day 041](../daily/day-041.md) shipped [the week-six map](../integration/week-06-the-loop-meets-the-model.md), the weekly page putting that week's pieces into one picture, and its diagram. The first version ran an arrow from the eval straight to the handoff packet. The change-control standard, written two days earlier, routes a configuration change through [the builder self-check](../enablement/builder-self-check.md), the builder's own pass before handoff, and carries the eval result in the packet. The arrow had to land a step earlier. Prose tolerates a vague join; an arrow has to pick a node.

[Day 044](../daily/day-044.md) shipped [the maintenance policy](../governance/maintenance-policy.md), which settles what this repo owes once the daily entries stop. Its first obligation was going to be "the CI stays on." [The checks workflow](../.github/workflows/checks.yml), the CI running this repo's one automated check, fired on push and pull request only, and a finished repo does not push, so the obligation that leans least on somebody remembering would have been vacuous the day it took effect. A weekly schedule and a manual trigger went in the same day.

A smaller one, from [Day 045](../daily/day-045.md). My draft of [the adoption guide](../enablement/lifting-this-into-a-real-team.md), the path a new team follows, said the review log has four required fields. The spec requires five, and three passes caught it separately.

What none of that establishes is a rate. A catch is visible and a miss is not, so four of them say nothing about how much went through unexamined.

Drafting this note turned up one of the misses. The log spec had said four required fields since its first version, when four was right. A later version added a fifth, updated the field list, and left that line alone. It said four for seventeen days, across two version bumps, in the file the review side reads most, and every pass over it read past that line. It is corrected now, in the same commit as this note, with the version bump [the maintenance policy](../governance/maintenance-policy.md), which settles what this repo owes after the daily entries stop, requires.

Nothing here could have caught it. [The index check](../checks/check_index.py) tests paths, titles, versions, and one tally on one page. A file disagreeing with itself in prose is the drift its own notes say a person has to find. The checking works when it is pointed at something, and this is a measured instance of it pointing elsewhere for two and a half weeks.

## What this does not claim

Checking is a narrow instrument. It settles whether a claim holds, which is what every catch above is. Whether a sentence is worth reading is a different question, and the prose is mine to answer for.

The bigger limit has a name here already. The drafting and the checking run on the same system, from the same brief, prompted by the same person. A mistake both are prone to survives every pass, and there is no outside auditor. That is the trust-relocation problem the spot-audit guardrail names, applied to what you are reading: the word moved from the draft to the check, and it did not go away. I am not the cover for it. I originate the brief and I approve the result, which by this repo's own audit rule is a disqualified position. What partly covers it: the record is public and dated, so every claim this note makes about the repo can be checked. The claims it makes about me cannot be. That I read every file leaves no artifact, and a reader who wants to discount it should.

The data is still synthetic. The ground rules on the front page say so, and nothing here has run with a real team.

## What you can do with this

Every catch above cites a dated entry you can open. Clone the repo and the index check runs in a second: it exits clean or hands you the file that broke. The rest is the ordinary work of reading an argument and seeing whether it holds. This note tells you what produced the arguments, so you can weigh them the way you would weigh anybody's.

---

*v1. A living note. The next pass records what this method looked like from the outside, once somebody other than me tried to reproduce a day from its brief.*
