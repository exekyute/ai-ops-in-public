# Reviewing Without Rubber-Stamping (v1)

You are about to review someone else's build. A review is a control only if it actually looks. A rubber
stamp is a review that marked the checklist lines off evidence that does not answer them, the clearest
case being "it runs, so the secrets must be fine." This guide is the habits that make your review real,
written for someone reviewing for the first time. It is the reviewer's side of the same quality bar the
builder self-checks against in `enablement/builder-self-check.md`, and it assumes you are running
`sops/run-a-build-review.md` with `governance/ai-build-review-checklist.md` open.

## What a rubber stamp actually is

Hold one idea before you open the checklist: your whole job lives in the gap between "the build works" and
"the build is fine." The build in front of you works, or the builder would not have handed it off. Whether
it works is easy to confirm: you run it and watch. Whether it is fine is a different question, and on some
lines the run gives you no sign either way. Closing that distance is the entire reason you are here.

A rubber stamp is more than a lazy reviewer skimming and clicking approve. The reviewer in Day 022's
example (`examples/a-rubber-stamped-approval.md`) did real work: they read the description, ran the happy
path, ran the bad input, and walked the Basics. The stamp was one line. They marked "secrets are in the
credential store" as a yes because the build ran, and a running build says nothing about where the secret
lives. The token was sitting in the node's authorization header, in plain view of anyone who opened the
node, and nobody opened it.

So a rubber stamp is a category error before it is sloth: a line marked off evidence that does not answer
the question the line asks. Some lines a run can settle, and some it cannot, and the trap is answering the
second kind with the first kind's evidence. The most valuable thing you do is the thing a working build
gives you no reason to do: run the bad input, open the node.

## The habits

Four habits turn the review from a box-tick into a real look. Each one is a way of closing the gap the
working build hides.

### 1. Run it, and run it mean

Run the happy path, then a bad input, then the same input twice. The happy path is the weakest evidence
you have, because it shows the one case the build was made to handle. The problems live in the other two
runs.

- The bad input shows whether there is an error path at all, and whether a person gets told when something
  fails.
- The same input twice shows idempotency. Day 015's build (`examples/a-build-through-the-loop.md`) posted
  one clean reminder on the first run and a second identical reminder on the second, and the double-post
  only appeared because the reviewer ran the day through twice. A single clean run was silent on it.

Run all three every time, even when the happy path looked clean. Especially then. If you only run the
happy path, you have confirmed the one case nobody was worried about.

### 2. Open the thing on the lines a run cannot answer

Some checks a working build gives no sign of: secrets, key scope, retries, versioning, owner. On these
lines a build that passes and a build that fails run identically, so "it runs" is not "I looked."
`governance/inspection-required-checks.md` names each of these lines and says exactly what to open: the
auth field on the node, the scopes on the credential, the version history, the owner register. A token
typed into an authorization header and a token pulled from the credential store make the same successful
call, and the only place the difference shows is inside the node. So open the node, open the credential,
open the register. A yes on one of these lines without an open node is a yes with nothing behind it.

### 3. Decide from the marks, not your gut

The review has three outcomes, and they come from `sops/run-a-build-review.md`: Approve, Approve with
fixes, Send back. Let the filled-in checklist make the call.

- All checks pass: Approve.
- Passes except for small, clearly listed fixes: Approve with fixes.
- Any Basics, ownership, or lifecycle check fails, or the build does not do what the description says: Send
  back.

Deciding from the marks is what makes two reviewers land in the same place on the same build. A gut call
("this feels fine") stays in your head, so a second reviewer reading the same build can land somewhere
else. A filled checklist is shared, so it travels, including to the auditor who checks your work later.
When the marks say send back and your gut says approve, go with the marks, because the marks are what you
can defend in an audit.

### 4. Write the reason

The filled-in checklist is your message back to the builder. One clear reason beats a vague "this looks
off," because the builder can act on the first and can only guess at the second. Day 015's reviewer wrote
exactly what failed and the fix: re-running the day double-posts, the Slack step has no dedup key, add a
dedup on invoice id plus due date. The builder read that and knew what to do without a meeting. Write the
check that failed, what you saw when you ran or opened it, and what would close it. That reason is also
what an auditor reads to see whether your call held up.

## You will be audited, and that is the point

Your approvals get re-reviewed. A spot-audit (`governance/review-spot-audit.md`) pulls a small random
sample of already-decided builds, weighted toward the ones you approved, and a second person (not you and
not the builder) re-reviews them cold against a fresh checklist, opening the same node you were supposed
to open. When their decision differs from yours, that is a review miss, and the review miss rate counts
it. The one that matters most is an approval the audit would have sent back, because the send-back rate
cannot see that one by construction.

This is a feature of the role, not a trap laid for you. A rubber-stamped build looks exactly like real
prep from the outside: submitted, reviewed, approved, no bounce. The audit is the only thing that can tell
those two apart, which is why it exists. A miss is a calibration, not a charge
(`enablement/handling-a-review-miss.md`): sometimes it is a judgment call the standard left open, and
sometimes the audit is the one that got it wrong.

Nobody expects you to never miss. What is expected is narrower: that your approvals hold up when a second
person opens the same node you did. That is the whole test of a real review: it survives a cold re-review.
If you opened the node, ran the bad input, and decided from the marks, your approvals will hold, and the
audit becomes a confirmation that you looked.

## Going slow is fine

Be honest about what this guide can do. It can teach the habits. It cannot install the care.

Your first reviews will be slow. You will open nodes you could have assumed were fine, run inputs that
pass, and read scopes line by line. That is the job done right. A slow real review beats a fast rubber
stamp, because the fast one skips the thing a review is for.

The habits get faster with practice. Running mean, opening the node, deciding from the marks, and writing
the reason all speed up once they are muscle memory, and a review that took an hour cold takes a fraction
of that once you know where to look. What stays slow to earn is the care: the willingness to open a node
on a build that already works, when nothing is forcing you to. Nothing here turns a reviewer who does not
want to look into one who does. It gives a reviewer who does want to look the moves that make the looking
count. The care is the part that has to stay.

---

*v1. A living guide. The next pass folds in the reviewer moves that held once a new reviewer ran their
first real review and their first cold audit, and tightens any habit a miss showed was too loose.*
