# Week 6 Log

Days 036 to 041. Week 1 was breadth, week 2 depth, week 3 turned the loop on itself with an audit, week 4 scaled it to a pool of people, and week 5 kept what those weeks wrote. This week the repo looked at itself twice. Once at its rules, where a specification with nothing running it turned out to be a rule nobody had to keep. Once at its own writing, which I read cold and could not follow. Six days, six artifacts, one change to the front door, and the first code in here.

## What shipped

- [`checks/check_index.py`](../checks/check_index.py): v1, the first code in this repo, four rules over [the review-loop index](../sops/the-review-loop-in-order.md), the start-here page for the review side. [The measure-or-test memo](../analytics/measure-or-test.md), the ruling on when a question wants a number and when it wants a test, had specified all four, two of them run once by hand and two never at all. The first run exited 1 on real drift in the two files that had each predicted, in writing, that they would be the first things caught.
- [`.github/workflows/checks.yml`](../.github/workflows/checks.yml): v1, CI running the script on every push, so a broken pointer fails the build where anyone can see it. [The check's notes](../checks/README.md) went to v2 and deleted their own "nothing runs it automatically" limit one day after writing it.
- [`enablement/where-a-human-stays-in-the-loop.md`](../enablement/where-a-human-stays-in-the-loop.md): v1, two design-time questions, what undoing a wrong output takes and whether anything would notice it, resolved on a grid into one of four placements and recorded in a line beside the build. [The review checklist](../governance/ai-build-review-checklist.md), the gate a build passes before it goes live, has asked since its first version whether a person is in the loop wherever the stakes are real. That line had been unanswerable for thirty-six days.
- [`standards/prompt-and-model-change-control.md`](../standards/prompt-and-model-change-control.md): v1, prompt text, model id, decoding parameters, tool definitions, output schema and grounding source under one procedure, with a dated pin so a provider-side change becomes an event. It extends section 9 of [the automation standard](../standards/automation-standards.md), written for a workflow definition you can export, which does not reach a string in a parameter field. Its move: a configuration change is a handoff.
- [`analytics/evals-and-the-review-loop.md`](../analytics/evals-and-the-review-loop.md): v1, what a saved graded set can tell you. Two subsets and two bars: a regression list where the bar is every case, and a representative list read as a rate. An eval gates a change; a placement gates a run.
- [`integration/week-06-the-loop-meets-the-model.md`](../integration/week-06-the-loop-meets-the-model.md): v1, the five mapped as one loop, carrying the repo's second diagram. The index now lists all five weekly maps, the other thing last week left open.
- [The front page](../README.md): reworked mid-week, the loop drawn for the first time and an ordered start-here path at the top.

## What I actually learned

A rule and its enforcement are different objects, and only one of them binds. The week opened by finding that this repo had been counting written rules as controls. What turned four specified index rules into a control was sixteen lines of YAML, which cost less than the paragraph arguing for the rule. Price the enforcement first. When it is cheaper than the rule, ship it and let the rule point at it. I had spent five weeks warning about the log nobody keeps and built the same shape into my own folder.

When a check cannot be answered from the thing being checked, move the decision rather than the wording. The instinct with "a person is in the loop wherever the stakes are real" was to write a sharper sentence. No sharper sentence exists. Stakes are a fact about consequences, consequences live outside the build, and no phrasing lets a reviewer read them off what is in front of them. The information sits earlier, with the person designing the step, who knows what undoing a wrong output would take and whether anything downstream would catch it. The guide asks those two questions at design time and hands the reviewer a written claim to test. The gate is no stricter, and it is now answerable.

Every claim I made this week got narrower under checking, and the narrow versions were better. The change-control draft claimed that change control has no vocabulary for a change with no changer. False: lockfiles, version ranges and self-patching operating systems are exactly that. What survived is smaller and truer, that the mechanism is old and the missing piece is a signal, because a library that moves leaves a diff and a model that moves produces prose that still parses. The evals memo was going to claim that a good eval upgrades the placement guide's second answer, whether a wrong output would be noticed. It cannot. A confident yes there covers every wrong answer including the ones nobody wrote down, and one failing case refutes it outright, so an eval can refute a detection answer and can never establish one.

Then the map's first diagram ran an arrow from the eval straight to the handoff packet, bypassing [the builder self-check](../enablement/builder-self-check.md), the prep a builder runs before a handoff, and contradicting the change standard written two days earlier. Prose had hidden it, because a sentence can say a change goes through review and stay true enough to pass. An arrow has to pick a node.

## What was thinner than I wanted

Nothing this week has run against a real model step. The placement guide's worked record is authored, no prompt has moved through the change procedure, and the eval set does not exist. Both worked builds in [`examples/`](../examples/), where the loop runs end to end on invented work, are model-free, one marking the self-check's model section not applicable, the other never raising it. A repo about running AI still has no worked example of a build that calls one.

The placement guide and the change standard between them name four edits to files they do not own, and none has landed. The checklist still asks its stakes question, and the self-check still has no placement line.

Grading a non-mechanical output has no answer here yet. Where the expected answer is a team id the comparison is mechanical. For a drafted email there is no key, so something has to judge quality, and a model judging a model is a review with no audit on it. The memo names the fix and nobody has built it.

The rewrite described below has the same problem. Five entries carry the new format, nobody has read them cold, and the person grading whether this repo is legible is the person who could not see it was illegible for thirty-six days. Under all of it, unchanged since week 3: none of this has run with real people. No queue anyone pulled from, no build handed to a second person, no audit by a third.

## Why the entries changed shape

One day into the week I opened this repo the way somebody arriving at it would, one file cold with no context. It did not work, and every reason was visible in the files themselves.

The daily entries were written as chapters. Not one document in the tree linked to another, so every cross-reference was a dead end a reader had to resolve by hand. Five weekly maps described a loop that grew every week and not one of them drew it. The front page's first move sent people to [the daily folder](../daily/), then thirty-six filenames in date order, with nothing saying where to start. The limits were stacked at the end of every file, so anyone skimming read the disclaimers as the summary.

From [Day 037](../daily/day-037.md) on, each entry opens on a headline carrying that day's idea in place of a pillar label, runs a dateline that counts the day out of forty-nine, and links every repo file it names with a clause saying what that file is. Days 001 to 036 keep their original format, because this repo does not rewrite its past.

A file that only makes sense once you have read the thirty-five before it is a file only its author can read. Writing for yourself and writing something legible are different jobs, and I had been doing the first while believing I was doing the second. The repo was accurate the whole time. Accuracy was doing none of the work of being readable.

## Where this ends

I am running this to Day 049, Sunday 9 August, and then stopping. Seven weeks.

I am stopping because of the material. The review loop now has every part it needs, down to a placement for model steps, a change procedure that reaches a prompt, an eval that gates a change, and a check that runs on every push. The design is finished. The evidence is not, and that is the honest reason 49 is the number: what is still open is a second person, a real queue and a live model step, and no further writing by one person closes any of the three. What is left is padding the loop with variations on pieces already here, or beginning a different system under the same name.

What I mean by finished is complete and maintained. The CI stays on, a red check gets fixed, a correction bumps a version, and the last week carries a maintenance policy naming the conditions under which this would reopen. Stopping at a defined point while the thing is whole is the alternative to trailing off, which is how repos like this one usually end.

Seven days are planned, on the record so the final entry can be read against them: the first automation that runs this repo's own handoff, that policy, a guide to lifting the loop into a real team, a field guide at the root for anyone arriving cold, and a count of what this turned out to contain. If the automation does not land, the last entry says so.

The streak is at forty-one days. Last week's log set a test for this one: week 6 would either generate its own agenda the same way or the claim was a coincidence with a good name on it. All six subjects came due from limits the repo had written about itself and left standing. The one thing I chose was to sit down and read the tree cold. Naming an ending is the same move one level up, deciding the shape out loud while there is still something to decide.
