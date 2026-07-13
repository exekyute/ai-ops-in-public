# A Rubber-Stamped Approval (v1)

This file runs one synthetic build around the same loop as Day 015
(`examples/a-build-through-the-loop.md`), and it ends the opposite way. Day 015's build was one the
reviewer caught: the reviewer ran the check the builder had only eyeballed, found the double-post, and
sent the build back. This one is the build the reviewer misses. Its first review lands on Approve, so the
send-back rate records nothing, and the flaw ships with it, until a later spot-audit pulls the approved
handoff and catches it. This is the case the audit exists for: a false approval, an Approve the audit
would have sent back, the one miss the send-back rate is blind to by construction. Everything here is
synthetic: the build, the token, the review outcomes, the audit, and the numbers are made up to show the
path, and the three roles are the builder, the reviewer, and the auditor, never real people, companies,
or vendors.

Day 015's own closing named this exact case as a counterfactual: had the reviewer eyeballed the same item
the builder eyeballed, the double-post would have shipped. This file makes that counterfactual concrete
and walks the whole week-3 audit loop catching the case it was built for.

## The synthetic build and its flaw

The build is named `feedback-form-to-crm`. A webhook receives a customer feedback form submission and
creates a contact note in a CRM by calling the CRM's API. That is the whole job: a form comes in, one API
call goes out, a note lands on the right contact. It is small, it is useful, and it runs.

The flaw is one line of configuration. The CRM API token is typed straight into the HTTP Request node's
authorization header, as a literal value in a node parameter, instead of being stored in the credential
store and referenced from there. The token is valid, so the call succeeds every time, and nothing about
the build's behavior looks wrong. The problem is where the secret lives, and that is invisible from the
outside, because a token in a header and a token pulled from the credential store produce the identical
successful call. You only see the difference by opening the node and looking at the field.

## Stage 1: The bar

Before the build moves anywhere, it has a baseline to meet, and it is the same baseline for the builder
and the reviewer. That bar is `standards/automation-standards.md`. This build calls an external API with
a secret, so several sections apply, but the one that decides its fate is section 5, secrets and access.
The standard states it plainly: "Secrets live in the credential store, never in node parameters, code, or
commit history." A token typed into a node's authorization header is a secret sitting in a node
parameter, which is the exact thing section 5 rules out. The checklist that enforces the standard carries
the matching Basics line: "Secrets are in the credential store, not typed into a step or sitting in the
code" (`governance/ai-build-review-checklist.md`). The standard and the checklist name the same pass
condition, both people share it, and this build fails it. Everything else the build needs (an error path,
a named owner, a versioned definition) the builder does prepare, and those hold. Section 5 is the one that
bites, and it is the one nobody checks by opening the node. What follows is how a clear, shared, broken
rule still gets marked passing twice.

## Stage 2: The self-check that eyeballs the secret

The builder runs `enablement/builder-self-check.md` top to bottom before handing anything off, and almost
all of it comes back clean, and honestly so. The happy path runs: a real-shaped form submission goes in,
one contact note lands on the right CRM contact. The failure path runs: a submission missing the fields
the CRM requires is surfaced to a person instead of writing a broken note. There is one named owner, a
safe stop on the webhook, a versioned export for rollback, and the one-paragraph "what this does and why."
All of that is real, and all of it passes for the right reason.

One item is where the trip goes wrong, and it is the secrets item. The self-check asks the builder to
confirm the credentials are in the credential store rather than typed into a step. The builder knows the
build works, has watched the API call succeed, and marks the item fine on that basis, without opening the
HTTP Request node to look at the authorization header. The reasoning feels safe: the call authenticates,
so the token must be set up correctly. What it skips is the difference between a working token and a
stored one. The token works either way. The check is about where the secret lives, not whether the call
succeeds, and answering it means opening the node. The item got confirmed by assumption, not by opening
the node. That is the eyeball, the same blindness the self-check's own closing section warns about: the
builder is close to the build and reads past the item they already assume is fine.

## Stage 3: The handoff

With the self-check marked clean, the builder assembles the handoff packet and crosses the handoff point
in `sops/hand-off-a-build-for-review.md`. The packet is the three things that SOP requires: the runnable
`feedback-form-to-crm` build in a form the reviewer can open and run, the one-paragraph description ("a
webhook takes a customer feedback form submission and creates a contact note in the CRM by calling the
CRM's API"), and confirmation that the self-check is clean, including that the build was run against one
good and one failing input, with an owner named and a rollback in place. The packet is complete on its
face, so the handoff is accepted and the reviewer takes over. It carries one claim the builder confirmed
by eye rather than by opening the node, the secrets item, and nothing in the packet flags that
difference. Everything downstream now runs on the packet, including that one claim.

## Stage 4: The review that rubber-stamps it

The reviewer runs `sops/run-a-build-review.md` against the build and fills in
`governance/ai-build-review-checklist.md`. Most of it is a real review. The description is read and clear.
The happy path runs and produces the contact note; the token is valid, so the call succeeds and it
matches the description. The failure input is surfaced to a person instead of writing a broken note. The
Basics march down the list and genuinely pass: the name says what it does, the steps are named, there is
an error path, a person gets told on failure.

Then the reviewer reaches the Basics line "Secrets are in the credential store, not typed into a step or
sitting in the code." Here the review does the one thing that makes it a rubber stamp. The reviewer sees
the same working build the builder saw, assumes the same thing the builder assumed, and marks the line
yes without opening the HTTP Request node. The token is sitting in the authorization header, in plain view
of anyone who opens that node, and nobody opens it. This is the honest-reviewer assumption failing in one
exact spot. The review is a real control only if the reviewer opens the node and looks, and here the
reviewer ran the inputs (which is real work) and then read the one check that needed the node open
instead of opening it. Every other check genuinely passed, so with the secrets item marked yes and
nothing else outstanding, the decision is Approve.

The reviewer files the checklist and, per `sops/review-log-spec.md`, writes one row in the review log:
the build `feedback-form-to-crm`, the reviewer, the first-review outcome Approve, and the date. Those
first-review fields are now fixed. A build that a real review would have sent back got an Approve.

## Stage 5: The audit that catches it

The send-back rate cannot see this handoff, because its first review was an Approve. From the rate's
point of view the build arrived ready and passed clean, and nothing in the send-back numbers ever points
at it. This is the blind spot the spot-audit exists for.

Some cycles later, a spot-audit runs, following `governance/review-spot-audit.md`. The auditor is a third
role, not the builder and not the reviewer who made the call. The audit draws a small random sample of
already-decided handoffs, and it weights the draw toward approvals on purpose, because a lax review does
its damage in the builds that were waved through, not the ones that were sent back. This handoff was an
Approve, so it sits in exactly the pile the sample is weighted to pull from, and it gets drawn.

The auditor re-reviews it cold, blind to the original marks, against a fresh empty checklist. They read
the description, put the good input and the bad input through, and walk the Basics top to bottom, the same
review the first reviewer was supposed to run. On the secrets line, the auditor opens the HTTP Request
node, the step neither the builder nor the reviewer opened, and there is the token, typed into the
authorization header. That is a plain section 5 violation and a no on the Basics secrets line, so the
auditor's decision is Send back.

Now set the two decisions side by side. The original review said Approve. The audit says Send back. They
disagree, so this is a miss, and it is the specific kind the audit is built to catch: a false approval,
where the original approved and the audit would have sent it back. The auditor records it the way the log
spec allows, filling the audit fields on the existing row: audited yes, audit outcome Send back, miss yes.
The first-review outcome on that row does not change. It still reads Approve, frozen, with the audit
fields added beside it. One row now carries both stories: a clean first-review Approve the send-back rate
counts as a pass, and an audit Send back the review miss rate counts as a false approval.

## Stage 6: The numbers

Read what each number saw, using `analytics/metric-definitions.md`. Take this one handoff's contribution
to each, and do not read a rate off a single build.

The send-back rate counts first-review send-backs over handoffs reviewed. This handoff's first-review
outcome was Approve, so it adds zero to the send-back numerator. It adds one to the denominator, as a
handoff that was reviewed, and that is all. Read on its own, this build looks like clean prep: submitted,
reviewed, approved, no bounce. The send-back rate says nothing is wrong here, and it is not lying. It
counts exactly what it counts, the first-review outcome, and the first-review outcome was Approve. The
metric freezes that outcome for a reason, so a build cannot come around the loop and erase its own bounce,
and here that same freeze means the Approve stands in the count even after the audit overturns it. The
send-back rate cannot see this miss, and it is not built to. It measures whether builds arrive
review-ready, not whether the reviews hold up.

The review miss rate is the number that sees it. In the audit cycle that pulled this handoff, the audit
overturned the decision, so this row is one overturn (the audit decision differed from the original) and,
more sharply, one false approval (original Approve, audit Send back), the subset the metric definition
calls out as the one the send-back rate cannot see. The send-back rate scored this handoff zero; the
review miss rate scored it one overturn and one false approval. This one build does not make a rate on its
own, and reading a single cycle as a trend is a mistake the metric warns against. The point here is
narrower: the send-back rate said nothing, and the review miss rate is where the miss finally shows up as
a number.

## Stage 7: The miss conversation

The audit found the miss, and per `enablement/handling-a-review-miss.md`, finding it is worth something
only if the conversation after it makes the next review sharper. The first move is to name which kind of
miss this is, out loud and together. A judgment call is where the standard left room and two careful
reviewers read the same build differently, and this is not that kind: section 5 is unambiguous, the
checklist line is unambiguous, and the token was plainly in the authorization header. This one is a real
gap, a check marked passed without being run, where running it would have caught the problem. Anyone who
opened the node would have seen the token. Nothing here is a close call.

So the conversation is short, and it stays on the build. It opens from the build: two reviews of this
build landed differently, here is the check that split them. The check is the secrets line, and running it
means opening the HTTP Request node and looking at the authorization header. The standard settles which
reading is right (section 5 is plain, so the audit's Send back is the correct call), and the fix is one
habit: on the secrets line, open the node and look, do not infer it from the fact that the call works. It
is delivered as a habit to fix, not as a charge. "You approved a bad build" would leave the reviewer one
move, to protect themselves, and the review would stop meaning anything, which is the rubber stamp the
audit exists to catch. The useful thing to notice is that the same eyeball happened twice: the builder
marked the secrets item without opening the node on the self-check, and the reviewer marked it without
opening the node on the review. The habit that closes it is the same on both sides. Open the node. Run the
check.

## What this shows and what it does not

This shows the case the send-back rate is blind to. A build broke a clear, shared rule, both the builder
and the reviewer marked the rule met without opening the node, the reviewer approved, and the send-back
rate scored the handoff a clean zero, indistinguishable from real prep. The spot-audit pulled the approved
handoff, re-reviewed it cold, opened the node, found the token, and turned an invisible Approve into a
recorded false approval the review miss rate can count. The whole week-3 loop did the job it was built
for: the guardrail on the reviewer caught what the guardrail on the builder could not.

It also shows one failure mode worth sitting with: the same eyeball failed twice. The self-check and the
review are two separate controls, run by two different people, and both slid past the identical item the
identical way, because a valid token gives no sign of where it lives. A review is supposed to be a second,
independent look that catches what the first one missed, and here it repeated the first one's exact skip.
Two separate controls collapsed into one look, taken twice.

It does not prove more than one build's worth. This is one synthetic handoff with one planted flaw, a
secret in a header, chosen because it is a clean example of a check that passes by eye and fails on
inspection. A single miss is a record, not yet a pattern, and the miss conversation treats it as exactly
that, one habit to fix and not a verdict. The audit caught it only because this handoff happened to be one
of the few pulled in the sample. Had it sat in the approvals the sample did not draw, the token would
still be in the header, the Approve would still read as clean prep, and nobody would know. The audit
lowers the odds that a rubber stamp pays off. It does not drive them to zero, and this trace shows the
catch, not a guarantee of it.

---

*v1. A living example. It is the false-approval counterpart to Day 015's caught build, and it makes
concrete the counterfactual that example named, showing the spot-audit and the review miss rate catching
an Approve the send-back rate scored as clean. The next pass runs a third synthetic build whose
rubber-stamped miss is a judgment call rather than a real gap, so the miss conversation has to settle a
genuinely ambiguous line instead of a plain one.*
