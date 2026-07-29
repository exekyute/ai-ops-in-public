# Where a Human Stays in the Loop (v1)

A build calls a model. The model returns an answer, the build acts on it, and the run finishes green. A person may need to look at that answer before the build acts, and somebody has to decide whether this is one of those steps. Deciding it by feel is how the same build gets waved through by one reviewer and stopped by another.

[The review checklist](../governance/ai-build-review-checklist.md), the gate a build passes before it goes live, has a short section for builds that call a model. Two of its four lines do not say what would make a reviewer wrong:

- The output is checked before anything acts on it.
- A person is in the loop wherever the stakes are real.

The checklist opens by stating what it is for: two different people running the list should land on the same decision. Those two lines cannot deliver that. "Real stakes" is a gut call, so the mark records the reviewer's nerve that week rather than a property of the build in front of them. A reviewer having a calm week marks it yes. The same build, reviewed by someone who got burned last month, gets a no. Neither of them can be shown wrong. "Checked" has the same hole one level down: it does not say checked by what, against what, or before which step.

This guide replaces the gut call with two questions you answer while designing the model step. A grid turns your answers into a **placement**: where a person sits relative to that step, chosen from four options. It ends in one line written next to the build. A reviewer checks that line instead of guessing.

## Why the error path does not cover this

The usual instinct is that this is already handled. Section 2 of [the automation standard](../standards/automation-standards.md), the bar every build here is judged against, requires an error path: a failure tells a person, with the build name, the failing input, the error, and a timestamp. Put a person on that alert and the bad cases come to you.

That covers a call that fails. It does not touch the failure that matters on a model step. A model that returns a wrong answer in the right shape produces a successful run. The schema validates, the field is populated, the value is the right type, and every step downstream does exactly what it was told. Nothing raises. Nothing alerts.

Follow that into the numbers. The exception rate in [the metric definitions](../analytics/metric-definitions.md), the file that pins down each number this repo counts, is the share of runs that ended in an error or were handed to a person. A run where the model was confidently wrong and the build acted on it ended in neither. It scores as clean: started, finished, no human needed. The best-looking week an automation can post is the week it was quietly wrong at volume.

This shape has a name here already. [The inspection-required checks](../governance/inspection-required-checks.md), the file that sorts checklist lines by what can actually answer each one, calls it category 3. A build that passes the check and a build that fails it run identically, so no run is evidence either way. It is also the shape of [the rubber-stamped approval](../examples/a-rubber-stamped-approval.md), a worked run whose flaw passed two people and scored a clean zero on the send-back rate, the share of handed-off builds a reviewer bounces, which cannot see a false approval by construction. A cold re-review caught it later. A number read clean and something bad had shipped.

Borrow the label carefully, because a model step is not quite the same animal. On a configuration flaw nothing on the run is evidence, and the fix is to open the node once and read the field, after which the answer holds until somebody edits it. On a model step no automatic signal is evidence either way, for the same reason: the wrong output and the right one produce identical successful runs. The difference is that the evidence is sitting on the run, in the output itself, so a person who reads it can settle it. That is why every placement below is somebody reading output, and why category 3's answer, open it once, does not transfer. There is a fresh output on every run. The failure never announces itself, so the placement has to be decided while the step is being built, before the first run, and it holds until someone re-decides it.

## The two questions

**1. If this output is wrong and the build acts on it, what does undoing it take?**

- **a.** You can reverse it yourself, in the same system, and nobody outside the team has acted on it yet.
- **b.** Undoing it needs somebody else, or a correction has to go out to someone who already saw it.
- **c.** It cannot be undone. Money moved, something was deleted, or a person outside the team acted on it.

**2. If it is wrong, does anything notice?**

- **a.** A machine rejects it, every time. A wrong answer would fall outside the enum, out of range, or be an id that does not resolve. If a wrong answer can be a valid member of the set your validator allows, this is not 2a.
- **b.** A person notices later, on a cadence, from the record.
- **c.** Nothing notices. A wrong answer in the right shape flows through and reads like a right one.

Answer question 2 about the systems that exist today, and about wrong answers rather than malformed ones. A validator checks shape, not truth, so steps land on 2c more often than teams expect. A build with three model steps runs this three times, because the answers can differ from step to step.

## The four placements

Cheapest first.

1. **Machine check only, no person.** A validator on the output before anything acts on it: shape, allowed values, ranges, ids that resolve. Anything that fails goes to the error path.
2. **A person on a sample, after the fact.** Output ships, and a named share gets read later on a cadence by someone who can say whether it was right. What they find goes back into the rule or the prompt.
3. **A person on the exceptions.** The build routes outputs that fail a rule to a person and ships the rest.
4. **A person on every one, before it acts.** The model drafts, a person approves, and nothing leaves without a click.

Every placement includes placement 1. It is the floor under the other three, never an alternative to them, because a person reading malformed output is a person doing a machine's job. That floor is what the checklist line "the output is checked before anything acts on it" has been asking for all along. The other three say who looks on top of it.

Placement 3 needs a routing rule, and in a 2c cell that rule cannot route on wrongness, because nothing detects wrongness. It routes on proxies for it: the model's own reported confidence, or an abstain option you put in the prompt and act on; an output that falls outside a small usual set; a segment where a mistake is expensive, a named account or anything touching legal or safety; and a fixed random slice as the floor when no proxy fits. Pick a proxy you can read off the output at run time and write it down. Which proxy, and at what threshold, is the open question at the end of this file.

## Which placement the answers pick

|                                                | **1a** you undo it yourself | **1b** someone else, or a correction goes out | **1c** cannot be undone |
|------------------------------------------------|:---:|:---:|:---:|
| **2a** a machine rejects it, every time         | 1 | 1 | 4 |
| **2b** a person notices later, from the record  | 2 | 2 | 4 |
| **2c** nothing notices                          | 2 | 3 | 4 |

Take the cheapest placement the grid allows, and no cheaper. Five things the grid is saying:

- **Irreversibility outranks detection.** The whole 1c column is placement 4. A true 2a rejects every wrong answer you modeled, and it rejects them before the act, so those never reach the irreversible step. What it cannot reject is the wrong answer nobody thought of, and 1c is the one column where that residue cannot be walked back. The exception is narrow and worth saying out loud: if the wrong answers are a closed set and the gate blocks all of them, the bad output never gets acted on, and the step was 1c only on paper. Most steps that feel like that are 2c with a validator in front.
- **The trap case is 2c with 1b.** Nothing notices, and the correction has to go out to someone who already saw the wrong thing. That is placement 3 at minimum, and in that cell the routing rule matters more than who the reviewer is. A rule that routes the wrong 10 percent beats a careful reviewer reading a sample that never contains the misroutes.
- **2a with 1a is placement 1.** A machine rejects it and you can reverse it. This is the cell teams over-govern, putting a person on output a validator already settles.
- **Placement 2 shows up for two different reasons.** At 2b, a person is already reading the record, so placement 2 writes down a cadence and a share that exist informally. At 2c with 1a, nobody is reading anything, so placement 2 creates that read from nothing.
- **Placement 4 has a ceiling.** It is real only while one person can honestly read every output before the next batch arrives. Past that the grid has run out, and the answer is to change the step rather than the placement: narrow what the model decides so fewer outputs are irreversible, split the volume across approvers, or put the irreversible action behind a batch a person releases.

## What gets written down

Section 8 of the standard (ownership) says a production build names one owner, recorded next to the build or in a register. The placement goes in the same place, the same way:

    inbound-email-route-to-team, model step "pick the team":
    reversibility 1b, detection 2c, placement 3 (person on the exceptions).
    Routing rule: any email routed outside the 3 teams that take 90 percent of volume,
    plus a random 5 percent. Chosen 2026-07-29 at 60 emails a day.

That build reads an inbound email and picks which team it goes to. A misrouted email has already landed in another team's queue, so undoing it means a correction to the team that got it and a handover to the team that should have had it (1b). The model returns a team id that exists and parses, and a plausible wrong team reads exactly like a right one (2c). "Somebody will probably say it is not theirs" is a hope. Name the detection or mark it 2c.

Expect one thing from that record. Placements 3 and 4 turn routed runs into exceptions by construction, since the exception rate counts any run handed to a person. The metric definitions already ask you to decide per workflow what "routed to a person" means and write it down next to the build, so this line does that job too. On a placement-3 build the exception rate reads as the routing share, and you read it against the rule and the volume rather than against zero.

Two files in the loop need one edit each, and neither has landed yet. Section 4 of [the builder self-check](builder-self-check.md), the prep a builder runs before handing a build off, has four items today and none about placement. It gains a fifth: declare the placement, with both answers, the routing rule if there is one, and the volume. On the review side, the AI-steps line stops asking about stakes. It becomes three things a reviewer can settle: the declaration exists, the placement matches what the two answers pick, and the build implements what it declared.

Two of those three are a read of the record. The third means opening the build to see the validator and the routing or approval step, which is inspection work of the kind a passing run cannot answer. A reviewer can be wrong about all three and be shown wrong. Two reviewers now land in the same place on the same declaration, and where they disagree, they disagree about a written answer.

## What this does not settle

It does not set the threshold. The proxies above say what a placement-3 rule can read. They do not say where to draw the line, and drawing it badly routes everything or nothing. That rule is a check in the sense [the measure-or-test memo](../analytics/measure-or-test.md), the ruling on when a question wants a number and when it wants a test, gives the word: you can settle it on each output as it arrives. The number that sets its threshold is the error rate placement 2 exists to produce. Both are the next thing this repo takes up.

A placement also carries the volume it was chosen at, which is why the volume and the date sit in the recorded line. Placement 4 on 5 outputs a day is a real look. At 500 a day the approval is a keystroke and the record shows a human in the loop where there is none, which is the same category error named in [reviewing without rubber-stamping](reviewing-without-rubber-stamping.md), the reviewer's habits guide: a mark made off evidence that did not answer the question. The trigger is in the record. When volume doubles from the figure written there, the placement gets re-decided, and the owner reads that line on the same cadence section 8 already has them reading the build's health metric.

The last limit has no mechanical answer. This file cannot price a wrong answer for you. Reversibility is a judgment about your own systems and your own people, and two teams can honestly answer question 1 differently about the same step. Writing the answer next to the build turns that difference into something visible and arguable instead of a silent assumption living in two people's guts.

## Running it on your next build

Name the model step. Answer question 1, then question 2, in the words above rather than your own. Read the cell. Build the validator, because it is the floor under every cell. Add whoever the cell names, plus the routing rule if the cell is placement 3. Write the one-line record next to the build, and hand it off.

The decision moves out of the review and into the design, made by the person who knew the most about the step, at the moment it was cheapest to change. What reaches the reviewer is a written claim they can test.

---

*v1. A living guide. The next pass names the routing rule a placement-3 build uses, which proxy and at what threshold, and runs the grid on a second model step whose answers land in a different cell.*
