# Lifting This Into a Real Team (v1)

Every other guide here tells you how to run a role you have already been given. Nobody has given you one yet. What you find is a couple of dozen review-side pieces across six folders, and nobody adopts a set that size.

Take three of them. [The automation standard](../standards/automation-standards.md), the bar a build is judged against. [The review checklist](../governance/ai-build-review-checklist.md), the gate that turns that bar into a decision. [The reviewer's steps](../sops/run-a-build-review.md), which say to open the build, run one good input and one bad one, then walk the list.

This guide is what to take first, what to rename, and what will break.

## What to take first

Six stages. Two things fix parts of the order: the audit needs a third person, and every number needs log rows, so those cannot come first whatever you prefer. The rest is reasoned from how the pieces depend on each other.

**1. The standard, the checklist, and the reviewer's steps.** [The front page](../README.md) calls the first two the pair a team could lift today. The builder hands over a one-paragraph description of what the build does and why, a second person runs it and walks the checklist, and the checklist ends on one of three outcomes: Approve, Approve with fixes, Send back. The filled-in checklist is the message that goes back, so the review needs no separate write-up. [The ordered index](../sops/the-review-loop-in-order.md), which lists every piece by when you would need it, is where you go once you want more than these three.

**2. The builder self-check.** [The builder's copy of the same bar](builder-self-check.md), run before a build is handed over. Add it when reviews start bouncing on the same few items: no plain description of what it does, no owner named, no failure case run.

**3. The review log.** [One row per handoff](../sops/review-log-spec.md), five required fields, including who reviewed it and the date it was handed off. Those two carry weight later: the audit samples by reviewer, and the wait-time number cannot be computed without the handoff date. Before there is a queue, take that date from the moment the build was handed over. Start the rows at the first handoff. Everything else here can be picked up late, and rows cannot.

**4. The queue.** [The ordering and assignment rules](../sops/run-the-review-queue.md) for builds waiting on a decision, which also route each build around its builder. Add it only when builds start waiting on each other.

**5. The spot-audit and the review miss rate.** [A cold re-review of a small sample](../governance/review-spot-audit.md) of already-decided builds, and [the metric definitions](../analytics/metric-definitions.md), where the review miss rate counts what the audit overturns. It samples from the log, so it needs rows. Start it on a cadence the week your pool reaches three independent people.

**6. The model-step pieces.** [Where a human stays in the loop](where-a-human-stays-in-the-loop.md) places a person against a model step and records that placement next to the build. [Change control for prompts and models](../standards/prompt-and-model-change-control.md) versions the prompt, the model id, and the decoding settings with the rest of the definition. Skip both if your builds do not call a model.

Then the rule that makes the order work: **take the next stage when a specific pain shows up, never because it is next on this list.** A control adopted before its problem arrives is overhead, and overhead is the first thing dropped when a week gets busy.

Stage 5 is the stated exception, and it has to be. A rubber stamp shows up as a clean record instead of as pain, and the send-back rate reads the same whether builds are genuinely ready or the reviewer stopped looking. Waiting for that stage to hurt means waiting forever, so put it on a calendar.

## What to rename

The vocabulary here is load-bearing, and some of it will collide with words your team already uses. Rename freely. Keep the definitions.

- **Handoff.** Here it means one build's whole trip through review, which [the handoff ruling](../governance/what-counts-as-one-handoff.md) settles precisely, down to when a returning build counts as a new one. If the word already means a shift change in your tooling, pick another and carry the ruling over intact.
- **Review.** This may already mean code review on your team. Say which one you mean every time, or give this one a different name.
- **Exception rate.** The share of a live build's runs that errored or fell out to a person. Ask whoever owns your operations reporting whether that phrase is taken before the first build goes live.
- **The three outcomes.** Approve, Approve with fixes, and Send back can take whatever your tools already call them, as long as the middle one keeps counting as a pass.

Rename in one pass, before the first handoff. These files cross-reference each other constantly, and a half-renamed set is worse than either name on its own. [The worked records](../examples/a-populated-log-and-queue.md) show the shape with synthetic build names in them.

## What breaks in the first two weeks

Six things go wrong early. Five are ordinary, and the first decides whether you have a loop at all.

**The reviewer turns out to be the builder.** Count the people before you count the reviews. The loop needs three distinct people to be fully itself: a builder, a reviewer who is not the builder, and an auditor who is neither. The queue rules are explicit about what each pool size buys you. A pool of two gives you a real review and no audit. A pool of one gives you a self-check wearing a review's name.

**Nobody fills the log.** It goes first, because the cost lands today and the payoff lands in a month. The spec puts the rule plainly: write the row when the review lands, because later is when it gets skipped. Name one person who owns that. [The returning-build check](keeping-the-review-log.md) is the second habit, for a build you have logged before.

**The send-back rate drops to zero and somebody celebrates.** The metric file says plainly that zero is a warning sign, and it says why. Read the clean-approval count beside the rate, and hand the reviewer [the guide for reviews that stop being real](reviewing-without-rubber-stamping.md), which costs nothing and needs no third person.

**"Approve with fixes" becomes the default.** It counts as a first-pass pass, so a stack of soft passes hides a prep problem behind a healthy-looking number. Track clean approvals as their own count and read the two together.

**Checklist lines get marked off a clean run.** [The inspection list](../governance/inspection-required-checks.md) names which lines a passing run cannot answer: a secret typed into a step, an over-scoped key, a retry sitting on a write that is not safe to repeat. A sound build and a broken one behave identically on all of them, so the only way to mark the line is to open the node and look.

**Somebody asks for the metrics in week one.** Three review-side numbers computed on a handful of handoffs describe that handful. Read the raw counts for the first month, put the handoff count beside any rate you quote, and let the trends wait.

## What this cannot do

None of this has been run by a real team. Every record in this repo was written by the person who wrote the specs behind it, so the path above is reasoned rather than reported. The first team to run it will find something in here that is wrong.

There is one thing to do with that. [The maintenance policy](../governance/maintenance-policy.md) names exactly this as the first of its conditions for reopening the work: somebody outside the repo runs the loop and says what broke. It is the only evidence one person working alone cannot produce, and the policy commits to versioned revisions that cite it.

What you can have in week one is smaller than everything described here and complete in itself: three short documents, one review, and a decision with the reason written next to it. A build gets checked by a person who did not make it, against a written bar, and there is a record of why the answer was what it was. That is what "someone says it is done" never had. Everything else here is what you add when it stops being enough.

---

*v1. A living guide. The next pass rewrites the staging order and the two-week list against the first report from a team that actually ran this.*
