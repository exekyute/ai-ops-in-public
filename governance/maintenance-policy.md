# Maintenance Policy (v2)

Every file in this repo whose title carries a version number ends the same way: an italic line repeating that version and calling the file living. Thirty-one do as this policy ships, and twenty-two of those go further and name what the next pass will do. Treat the counts as of today and the rule as permanent, since more versioned files land before the last entry. [The spot-audit guardrail](review-spot-audit.md) checks the reviewer the way [the review checklist](ai-build-review-checklist.md), the gate a build passes before it goes live, checks the builder, and its next pass runs a real audit against a filled log.

Every one of those lines was written by a repo that shipped something every day, and the cadence was what would have delivered on them. Once it stops, a reader who opens one of those files finds a commitment with nobody scheduled against it. The files do not know the cadence ended. They go on saying "next pass" in the present tense.

This policy settles what those lines mean from the last shipping day on, and what the "complete and maintained" in [the log that named the ending](../log/week-06.md) commits this repo to.

## The footers stay as written

The instinct is to edit thirty-one footers and take the future tense out of each one. Do not.

Two categories sit in this tree and they behave differently. [The daily entries](../daily/), the running narrative of one entry per day, are dated records of what happened on a day, and this repo does not rewrite them. A living doc is different. A line in one gets edited when it stops being true, and that has happened here: [the check's notes](../checks/README.md) deleted their own "nothing runs it automatically" limit the day after CI made it false.

A "next pass" line does not stop being true when the cadence ends. It stops being scheduled. Its accuracy holds and its meaning changes, and the fix for a meaning is a reading rule rather than twenty-two deletions.

**A "next pass" line is a named piece of open work with nobody assigned to it.** After the last shipping day it is what it always literally was: a name for something the file is missing, written by the person best placed to know. It carries no claim about when, or whether, anybody gets to it.

Every footer stays true under that reading. What drops away is an implied date the footers never wrote down.

This is the move [the start-here index](../sops/the-review-loop-in-order.md), the ordered reading path through the review side, already made: point at each piece and let the piece speak for itself. One file carrying a rule stays true longer than thirty-one restating it.

## What "maintained" commits to

First the word. A defect is a place where this repo does not do what it says it does. It comes in two shapes: a broken claim in prose, and a build that fails [the automation standard](../standards/automation-standards.md), the bar every build here is judged against. The obligations below cover the first. The disclosure rule further down covers the second.

Three obligations, and they start when the last entry ships. They cover every versioned piece and the automation. The daily entries and the weekly logs carry no version because they are dated records, so a factual error in one earns a dated note under the claim it corrects and nothing is rewritten.

1. **The check stays runnable, and a red result gets fixed.** [`check_index.py`](../checks/check_index.py), the index check, reads the start-here index and tests four mechanical claims it makes about the tree: every cited path resolves, every entry matches its file's H1, every in-scope file is indexed, and the opening tally recomputes. [The checks workflow](../.github/workflows/checks.yml) runs it on push, on pull request, on a weekly schedule, and on demand. That schedule has a fuse. GitHub disables scheduled workflows in a public repository after sixty days without activity, so on a repo that has stopped taking commits the weekly run switches itself off, which is this obligation's own failure mode arriving one level further out than the version that named it. What does not expire is the script: standard-library Python, a second to run on a clone, no setup. The durable promise is that the check remains correct and runnable by anybody, rather than that somebody here keeps watching it. A failure names what broke, except on the tally rule, which reports counts rather than a file.
2. **A factual error gets corrected, and the correction bumps the file's version.** A wrong pointer, an internal link that resolves to nothing, a claim contradicted by another file in this tree, or a claim about anything outside this repo that a reader can show is false. Showing it means naming the thing that contradicts it. Disagreeing with the reading is not showing. Each versioned piece carries its version in the H1 and repeats it in the footer, so a correction that arrives without a bump is a silent edit to a record.
3. **A dead external link gets repaired, or removed if nothing replaces it.** The whole tree holds three external links, all pointing at this repo's own GitHub, so this obligation is small and still owed.

A report of a broken link or a wrong claim arrives as an issue, which is where a red check already shows up.

Nothing else is promised: no commitment to add a file, extend an argument, answer a question this repo raised about itself, or land any named pass.

## What is not a trigger

- A better framing of an argument whose claims are all true.
- A sharper sentence, a tighter section, a paragraph that could lose a clause.
- Another metric beside the ones in [the metric definitions](../analytics/metric-definitions.md), the file that fixes what each number counts and how to read it.
- An idea that arrived a week late and fits.

Each of those is a genuine improvement, and each is the ordinary reason a project never ends. They arrive forever, each one small enough to justify on its own, and a repo that treats them as maintenance is still being written under a different word. A file whose v1 was correct does not need a v2.

## Four known defects, and the repo is still complete

[The handoff intake automation](../automations/handoff-intake/README.md), the workflow enforcing the packet rule at submission time, shipped carrying four named failures against the review checklist, each written up beside the build with its fix: no dedup key, no alert when a write fails, one credential with no environment split, and no read of its own execution log. The dedup key is the instructive one. Its fix is a submission id on the form rather than deduplication on the build name, because [the handoff ruling](what-counts-as-one-handoff.md), which decides when a returning build counts as a new arrival, makes a second queue row correct when a build genuinely comes back.

None of the four is scheduled to be fixed. Is a repo carrying four known unfixed defects complete?

Yes, and the reason has to be argued.

A defect written down where the thing lives is a different object from one nobody has found. Anybody who imports that workflow finds all four in the same file that tells them how to run it, named, with the fix for each. An undisclosed defect is a lie by omission, and the reader never gets that chance. The spot-audit guardrail makes the same argument one level down: what it buys is detectability, and a failure nobody can see gets priced at zero.

The rule that follows: **a known defect may stay unfixed, and it may not stay unwritten.** Anything found here after the last shipping day and left alone gets written into the file that owns it, in plain terms, with the fix named, and that edit bumps the version.

Two bounds, or the rule turns into a license. A defect that would mislead somebody following the file, or make the thing unsafe to run as documented, is not disclosable: that file or automation gets marked unfit to use until it is fixed or withdrawn. When a defect list does more work than the file under it, the file gets rewritten or removed.

## What would reopen this

Three conditions, each naming what it would produce. A reopen condition that does not say what comes out of it is a mood.

**Somebody outside this repo runs the loop with a real team and reports what broke.** This is the gap this repo has carried longest: no queue anyone pulled from, no build handed to a second person, no audit by a third. It is the only condition that yields evidence one person sitting alone cannot write. It earns revisions to [the handoff SOP](../sops/hand-off-a-build-for-review.md) and [the reviewer SOP](../sops/run-a-build-review.md), the two documented paths a build travels, and to the checklist, versioned and citing the report.

**A pointer that is wrong while the check is green.** The check's notes list what its mechanical rules cannot reach: meaning behind a correct path, a hand-maintained scope list, every other cross-reference in the tree. A reader showing one of those wrong is drift the check cannot settle, and the answer is a fifth rule or a second index. That is code, and it ships with a run that failed before it passed.

**A second system, under a new name.** Never a resumed count of days. The count here is a closed fact, and restarting it would retroactively make this ending a pause, which is the exact thing this policy exists to prevent. New work on this material starts elsewhere, with its own name and its own first entry.

## What this cannot do

A policy cannot make anybody maintain anything. That is the ceiling every guardrail here has already named, and this one inherits it: the checklist can be skipped, the audit run lazily, and this file ignored by the person who wrote it.

CI narrows that ceiling for as long as the schedule survives, which outlasts the cadence by about two months and not forever. While it runs, drift gets found without a person deciding to look, and a result shows on the badge at the top of [the front page](../README.md), the entry point carrying the check's status. After the schedule lapses the badge freezes on its last run, and that is worth knowing before anybody reads one: a green badge on a finished repo says the check passed the last time it fired, not that somebody is still watching. The four rules read one index either way, so it was always a narrow claim rather than a clean bill. The reliable move is to run the script yourself.

## What this file is

Every other control here sits inside the loop: the checklist gates a build, the spot-audit checks a reviewer, the index check tests pointers. This one sits on the repo, and governs a reader's ability to tell what they are holding.

A finished repo and an abandoned one look identical from outside on any given day. Nothing new, an old last-commit date, files unchanged since. What separates them is that somebody wrote down which of the two it is, what is still owed, and what would bring the work back. This file is that.

## What changed in v2

- Corrected the first obligation, which promised more than the infrastructure delivers. It read that
  the CI stays on. GitHub disables scheduled workflows in a public repository after sixty days without
  activity, so the weekly run expires on its own once the commits stop, and no wording here changes
  that. The obligation now rests where it holds: the check stays correct and runnable by anybody on a
  clone. The badge caveat moved with it.
- This is the failure the first version of this obligation was written to catch, found again one level
  out. A control tied to an activity dies with the activity, and a scheduled workflow turns out to be
  tied to the repository being active. Version one fixed the trigger and inherited the same shape.

---

*v2. A living policy. This line is unassigned like the rest, and the next pass records the first
correction somebody other than the author reported under these rules.*
