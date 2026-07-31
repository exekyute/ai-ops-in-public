# Evals and the Review Loop (v1)

Somebody edits two sentences of a prompt to fix a case the model kept getting wrong, and saves. The next question is whether the build got better, or whether that one case now passes while something else quietly broke. Nothing in this repo answers that, and two files have walked up to the question and stopped on purpose.

[The placement guide](../enablement/where-a-human-stays-in-the-loop.md) decides, at design time, where a person sits relative to a step that calls a model. It sorts every such step into one of four **placements**: a machine check only, a person on a sample after the fact, a person on the routed exceptions, or a person approving every output before it acts. A build on placement 3 routes some outputs to a person and ships the rest, and the routing rule fires on a proxy for wrongness: the model's own reported confidence, a value outside the usual set, a named account. The guide declines to say where that line goes, and it says why in one sentence: the number that sets the threshold is the error rate placement 2 exists to produce.

[The change-control standard](../standards/prompt-and-model-change-control.md), the rules that put a prompt, a model id, and the settings around them under version control, stops one step earlier. Its section titled "One run is not a test" requires the old configuration and the new one to run against the same set of inputs, because one run tells you about one input. It names two cases that belong in that set, the one that prompted the change and the ones this build has gotten wrong before, and it warns that a set of easy inputs agrees with every change you make. It does not say how big the set is, what the rest of it looks like, or what result clears the change for release.

Both gaps want the same object: a set of saved inputs, each with an expected answer, run against a model step and scored. That object is an eval. This memo places it against this folder's own ruling about numbers and tests, says what the set holds and what it has to clear, and draws the line around what it can buy you.

## The crux: a test on a sample

[The measure-or-test memo](measure-or-test.md), this folder's ruling on when a question wants a number and when it wants a test, split the world in two.

- A **metric** summarizes past events whose truth cannot be re-derived. The run happened, the review landed, and all you have left is what the record kept.
- A **check** settles claims about a present state you can read directly. Ground truth is sitting there, so the output is a list of what broke, or nothing.

Measure what you must estimate, test what you can decide. An eval lands cleanly on neither side, and saying exactly why is this memo's first job.

Case by case, an eval is a check. The model produced X, the expected answer is Y, they match or they do not. Nothing is reconstructed, the ground truth sits in the file beside the input, and you can run it again as many times as you like.

The set is where it breaks. What you want to know is how the step behaves on the input that arrives tomorrow, and you cannot run that one, because you cannot even write it down. The cases you saved are a sample of an input space nobody can enumerate, and the pass rate across them estimates something you never get to read directly. That is a metric's problem, sitting inside a thing built out of checks. So an eval is a test applied to a sample in order to produce an estimate.

The obvious objection is that the ruling already covered this. The sibling memo wrote that sampling is one way a metric copes, and that one of its four entries samples. The difference is what gets sampled. The review miss rate draws from the builds decided since the last audit, a finite list that exists today and could be read in full, and its blind spot is the rows nobody pulled. An eval draws from a space with no full to read, because tomorrow's input does not exist yet.

The same distinction resolves something that otherwise looks inconsistent. [The index check](../checks/README.md), the repo's only code and the only thing it runs automatically on every push, also fires when something changes, which makes it look like the same kind of control. It reads a **population**: every file in the scoped folders is sitting there, so exhaustive reading is available, which is why the measure-or-test memo could call a rate on it a lossy summary of a result you already hold. That memo rested its 100 percent bar on a separate argument, that a wrong pointer's whole cost lands on the one reader who follows it and a rate averages a cost that does not average. Either way, 100 percent on an eval's set stays silent about the input that was never in it.

That is why an eval carries a threshold and the index check carries none. The threshold is the written admission that the set is a sample.

## The shape is already here

[The spot-audit](../governance/review-spot-audit.md), the repo's only sampling control, pulls a small sample of already-decided builds, gives each a cold second review by a third person who was neither the builder nor the original reviewer, and counts a different decision as a miss. The draw is weighted toward approvals on purpose, because a lax review does its damage in the builds that were waved through.

An eval is that same shape pointed at the model. The spot-audit exists because the record cannot grade the decision-maker: a review that was waved through and a review that was run produce the same green row. A model step has the identical problem one level down, since a wrong output in the right shape produces a successful run. Both controls grade decisions the record cannot grade, one live and one saved.

Borrow the shape carefully, because the two sample for opposite reasons. The spot-audit could read its whole population and declines, because auditing everything relocates the trust problem one level up. An eval samples because there is no full to read. So the spot-audit's ceiling is detectability, and an eval's is the set's authorship.

The reading rules transfer anyway, because both are rates on small samples. The review miss rate, the share of audited reviews the audit overturned, is one of four entries in [the metric dictionary](metric-definitions.md), the file that pins down each number this repo counts, and it already carries what an eval needs.

- **Put the count next to the rate, every time.** A rate with no count under it says nothing. Write "94 percent of 50 cases."
- **A small sample swings.** On a 30-case set, one more failure moves the rate more than three points, so one run tells you about that run.
- **A sample weighted where failures hide works as a detector and fails as an average.** The spot-audit weights toward approvals and gives up being a fair estimate of the rate across all reviews in exchange.
- **Never read it alone.** The miss rate is read beside the send-back rate, the share of handed-off builds a reviewer bounces. A pass rate is read beside what the live build does: the exception rate, the share of runs that errored or fell out to a person, and whatever the person in the placement is finding.

## What the set holds, and the two bars

"What does the change have to clear" never had one answer, because the set is two subsets with two different bars.

**The regression subset.** Every case that ever caused a change: the case that prompted this prompt edit, which the change-control standard already requires you to include, plus every production failure anyone found and wrote down. Its bar is 100 percent, with no threshold. A case you already paid for once, failing again, is a failure full stop, and its cost lands on whoever it lands on instead of averaging across the cases that passed. You hold every case in it, so what you want back is the names of the ones that broke.

One rule keeps that bar clearable. A regression case encodes what was correct on the day the failure happened, and the change-control standard names the event that invalidates one: a change to what the step decides, rather than how well it decides it. After that change the old case correctly fails, and an unconditional bar on a list that only grows would block every change from then on. So a case leaves the set by moving to a retired list, carrying the change that retired it and the date, never by deletion, and retiring one goes into the change under review. Anyone can retire an inconvenient case. The retired list is what makes that visible and arguable.

**The representative subset.** Cases drawn to look like live traffic, with the ordinary ones included, in roughly the mix the step actually sees. A set of only hard cases produces a rate that describes hard cases, and no build runs hard cases all day. Its bar is a rate against a threshold, because it is a sample and there is no other honest way to read one. Size follows from what you plan to do with the rate: start at the smallest count where one failure moves the rate less than the difference you would act on, write that count next to the rate, and grow the list when the rate swings wider than the decisions it feeds. On 20 cases one failure is five points, wider than most thresholds are worth arguing about, so treat 20 as a floor.

The set is fed by the placement. Placements 2, 3, and 4 each put a person on live output, so each produces a labeled failure, an output somebody read and called wrong, and each of those becomes a regression case. Placement 4 produces the most, because a person sees every one. Placement 2 also produces the other half, since a person reading a sample labels every case they read, right and wrong, and a labeled right answer is exactly what a representative case is. Placement 3 does not: only the routed exceptions cross a person, so ordinary traffic there needs a separate labeling pass.

Run it backwards. A build on placement 1 has a validator and nobody reading output, so it generates no labeled cases, and its set only ever holds what its author imagined. The cheapest placement is the one whose set goes stalest, which is a real cost of the downgrade the next section argues for.

## An eval gates a change, a placement gates a run

An eval gates a change. A placement gates a run. They answer different questions and neither substitutes for the other. Shipping a configuration that scored 97 percent and then putting nobody on its output is the mistake this section exists to prevent: the eval spoke about the cases you collected, and it is silent about the output that ran an hour ago.

The placement guide's grid makes the boundary exact. Question 1 asks what undoing a wrong output takes: you can reverse it yourself (1a), somebody else has to or a correction goes out (1b), or it cannot be undone (1c). Question 2 asks whether anything notices a wrong output: a machine rejects it every time (2a), a person notices later from the record (2b), or nothing notices (2c). An eval is evidence about question 2 and no evidence about question 1. Reversibility is a fact about your systems, your permissions, and who outside the team has already acted, and no pass rate moves it. Two consequences follow.

**An eval refutes a detection answer and cannot establish one.** 2a says a machine rejects a wrong answer every time, and the guide adds that if a wrong answer can be a valid member of the set your validator allows, this is not 2a. That is a claim about every wrong answer, including the ones nobody wrote down, and a sample cannot certify it. One case where the validator passed a wrong answer settles the cell as 2c on the spot. A clean run settles nothing about the wrong answers you never collected. What establishes 2a is an argument about how the gate is built, a closed enum, an id that has to resolve, a range with no valid wrong value inside it, which is inspection work of the kind the change-control standard already routes to a reviewer opening the step. So a placement can drop when detection was what was missing, and it drops on that closure argument with the eval as corroboration. The eval's more common job runs the other way: it is how a team finds out a 2a answer was wishful. The change-control standard already requires the re-answering, since any change to the configuration re-opens both questions, and the placement guide says to take the cheapest placement the grid allows and no cheaper.

**An eval can never empty the 1c column.** The whole irreversible column is placement 4, a person approving every output before it acts, whatever question 2 answered. The guide names one narrow exception: if the wrong answers are a closed set and the gate blocks all of them, the step was 1c only on paper, and it warns that most steps that feel like that are 2c with a validator in front. An eval is how you tell those apart, since running every collected failure mode at the gate either shows the gate holding or hands you the counterexample. It cannot prove the set of wrong answers is closed, so it can support that exception and never create it. No pass rate buys you out of a person on a step that is actually irreversible.

Two thresholds come out of this, and collapsing them is why the question looked unanswerable. The **release bar** says what clears a configuration change: every regression case passes, and the representative rate sits at or above the old configuration's rate on the same list. Where that floor sits in absolute terms is set once per build from what a failure costs, which is question 1 of the same grid, and written next to the pinned model id. The **routing line** says which live outputs a placement-3 rule sends to a person, and a single pass rate cannot produce it, because a rate over the whole set says nothing about where the failures sit. What produces it is one more field on each representative case, the proxy value the rule would read: the reported confidence, or whether the answer fell outside the usual set. Then the set yields an error rate per proxy band, and the line goes at the band where the error rate stops being one the reversibility answer tolerates. That is the number the placement guide deferred, and it needs the field recorded from the first case on.

## What this does not solve

**Grading is the hard part, and it is the real ceiling here.** For a routing decision the right answer is known and the comparison is mechanical: the team id matches the expected id or it does not. For a drafted email or a summary there is no key, so something has to judge whether the output was good, and if that judge is a model then it is a review with no audit on it. That is the trust-relocation problem the spot-audit names, one level further out. What covers it is the spot-audit applied there: a person reads a graded sample of the judge's own calls on a cadence, disagreements are misses, and a judge whose verdicts do not survive a cold read is one you stop citing. This memo specifies that. Nobody has built it.

**There is no run history behind any of this yet,** so this memo is a specification, the way the index check was specified before anything ran it, and the sizing floor above is reasoned rather than measured. The first set has an obvious target: the email-routing step the placement guide already worked end to end, where the expected answer is a team id and the grading is mechanical. That first run is what tests the sizing rule.

## Whether the dictionary gains an entry

The measure-or-test memo refused to add a fifth metric and argued why, so the precedent gets tested here.

By the dictionary's rule for adding one, the representative subset's pass rate qualifies: it is hand-computable from the records it draws on, a list of cases and a graded result per case. Clearing that bar is also where the rejected candidate started, so run the three tests that sank that one. There is a healthy amount of failure on this rate, because a representative set carries hard cases and a build that gets every one right has a set that got easy. The rate is a claim about the traffic you did not run, so it summarizes nothing you already hold. And its trend is worth reading, since a pass rate drifting down across configuration changes on a stable set is the degradation the change-control standard's rollback section already names as a trigger on its own.

The regression subset's result does not qualify. It is a check, the same as the index: you hold every case, the bar is all of them, and the useful output is the names of the ones that failed.

So the dictionary gains one entry, later. Its denominator is the representative list, and the rule that draws that list is the part this memo set by reasoning, so the entry gets written once a real set exists and the sizing rule has survived contact with one.

## On your next configuration change

1. Write the set down as two lists, in the same place the pinned model id and prompt version already live next to the build.
2. Fill the regression list with the case that prompted this change plus every production failure anyone found. Grow it on every incident, and retire a case only in writing, with the change that made it wrong.
3. Fill the representative list with cases drawn to look like the traffic, ordinary ones included, and record on each the proxy value a routing rule would read.
4. Run both the old configuration and the new one against both lists.
5. Read the new configuration's regression result as a check, where any failure blocks. The old configuration's result on that list is the baseline showing which cases the change was meant to move.
6. Read the representative lists as rates, new against old, against the release bar you set from what a failure costs.
7. Put the result in [the handoff packet](../sops/hand-off-a-build-for-review.md), the bundle a build travels to review inside, with counts: 12 regression cases, all passed; 40 representative cases, 38 passed under the new configuration against 37 under the old; 5 outputs differed between the two, 4 wrong to right and 1 right to wrong, listed. The list of what moved is the part a reviewer reads, because a rate that held steady while five cases moved underneath it is a different event from one that held steady because nothing moved.
8. Re-answer both placement questions. The eval can move the detection answer. It cannot move the reversibility one.

That gives the change-control standard's set a definition, gives the placement guide a routing line it can draw from evidence, and keeps the person on the output where the grid still puts one.

---

*v1. A living memo. The next pass builds a real set for the email-routing step, runs a configuration change through it end to end, and writes the dictionary entry the representative pass rate has already earned.*
