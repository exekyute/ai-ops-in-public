# Checks a Running Build Cannot Vouch For (v1)

A review confirms a build against the checklist in `governance/ai-build-review-checklist.md`: you run the
build, walk the checklist, and mark each line. Day 022's worked example
(`examples/a-rubber-stamped-approval.md`) showed a build that ran perfectly and still failed the standard,
because a secret was typed into a node's authorization header instead of stored in the credential store,
and both the builder and the reviewer marked the secrets line passing because the build ran. The call
succeeded every time, so nothing about the run looked wrong, and "it runs" was no evidence at all for that
line. For some checklist lines a passing run feels like it settles the check when it settles nothing. This
file names the lines where that trap lives, so "it runs" never stands in for "I looked," and says exactly
what to open to answer each one.

## The three ways a check gets answered

Every mark on the checklist is answered one of three ways. Knowing which way a given line is answered tells
you what you have to do to mark it honestly, and whether a run can settle it at all.

1. **The happy path shows it.** Run one clean input and you can see it. "Does the build do the job the
   description claims" is this kind: a real-shaped input goes in, the right thing comes out, and the check
   is met in front of you. Most of the checklist sits here.
2. **An adversarial run shows it, and the happy path does not.** You have to run a bad input, run the same
   input twice, or force a failure. The error-path check, the failure-alert check, and idempotency all sit
   here. A clean run never fails and never repeats, so it shows you nothing. Day 015's build
   (`examples/a-build-through-the-loop.md`) was caught this way: the double-post only appeared when the
   reviewer ran the same day through twice, and a single clean run had looked fine.
3. **Only inspection shows it.** A build that passes the check and a build that fails it run identically, so
   no run is evidence either way. The difference lives in the configuration behind the behavior, not in the
   behavior, so the only way to answer the line is to open the config, the credential, or the register and
   look. Day 022's secret was this kind: a valid token typed into a header and the same token pulled from
   the store produce the identical successful call. The only place the difference is visible is inside the
   node.

Category 3 is the dangerous set, for one specific reason: a passing run gives false reassurance. "It runs,
so the secrets must be fine" feels like evidence while telling you nothing about the line in front of you,
because the broken build runs exactly as well as the sound one. That reasoning is what shipped the Day 022
flaw twice, once on the builder's self-check and once on the review. On a category-1 line a run shows the
answer; on a category-2 line a clean run visibly does nothing, so you know you still owe the failure run.
On a category-3 line the run looks like confirmation while answering a different question than the check
asked. The rest of this file lists the category-3 checks and, for each, what you open and what you look at.

## The inspection-required checks

Each of these is a real line on `governance/ai-build-review-checklist.md`. For each one a working build and
a broken build behave the same way, so the only way to answer it is to open something. The checklist line
and its standard section are named so you can trace each back, and they are grouped so related lines stay
together.

### Secrets and access

**Secrets are in the credential store, not typed into a step or sitting in the code.** Checklist Basics
line, standard section 5 (secrets and access), which states it plainly: "Secrets live in the credential
store, never in node parameters, code, or commit history." What to open: every node that authenticates
(look at the auth field), plus any Code node or committed file where a secret could sit as a literal. A
token typed into an authorization header and a token referenced from the credential store make the
identical successful call, so the run proves nothing. This is the Day 022 flaw exactly: the token sat in
the HTTP Request node's authorization header, in plain view of anyone who opened the node, and nobody
opened it. Confirm the secret is a reference to the store, not a literal value.

**Each key can only do what this build needs.** Checklist Basics line, standard section 5, least privilege:
"Scope tokens to the minimum the workflow needs. A workflow that reads a sheet does not need write access."
What to open: the credential itself, and read its scopes against what the build actually does. An
over-scoped key (write access on a build that only reads) runs identically to a tight one, because the
build only exercises the access it uses and never the extra it was granted. No run reveals the extra. You
have to read the scopes on the credential.

**Test and prod use separate credentials, with the env suffixed.** Checklist Basics line, standard section
1 (naming and environments): "never reuse one credential across test and prod. Suffix everything." What to
open: the credentials the build references, and check their names and environments. A reused or
wrong-environment credential runs fine, because the call succeeds either way. Whether test and prod are
actually separated is a fact about each credential's name and target, visible only when you open it.

### Retries

**Retries only happen on steps that are safe to run again.** Checklist Basics line, standard section 3
(retries and backoff): "Retry only idempotent steps. Retrying a non-idempotent write doubles the side
effect." What to open: each node that has a retry set, and reason about whether running that step twice is
safe. A happy-path run succeeds on the first try, so the retry never fires and you never see what it would
do. A retry on a non-idempotent write (a step that posts a message or creates a record) doubles the side
effect only when the retry actually fires, which is the run you did not see. Open the node, read what the
step does, and confirm a second attempt is safe.

### AI data

**No private or sensitive data goes to the model that should not.** Checklist AI-steps line, which the
checklist names as the section 5 access scope applied to model calls. What to open: what the build actually
sends to the model, and read the fields against what the model needs. A call that includes a field it
should not runs exactly like one that does not: the model returns an answer either way and the build
carries on. Whether a sensitive field is in the payload is visible only in the payload, so open the step
that builds the model input and read what is in it.

### Lifecycle

**The definition is versioned and revertible.** Checklist Ownership-and-lifecycle line, standard section 9
(change and rollback): "Workflow definitions are versioned, so you can see what changed and revert to a
known-good version." What to open: the version history or the repo, not the build. A build runs identically
whether or not you can roll it back, because the rollback path lives outside the running definition. Look
for the export, the commit, or the tool's version history, and confirm you could actually return to a
known-good version.

**One owner is named.** Checklist Ownership-and-lifecycle line, standard section 8 (ownership): "Every
workflow that runs in production names one owner." What to open: the register or wherever ownership is
recorded, not the build. A build runs fine with nobody accountable for it, and the run says nothing about
whether a name sits next to it. Check the record, confirm the name is there, and confirm it is one person
rather than "the team."

## What this is not

- It is a lens on the checklist, not a replacement for it. Every line named here is already a line on
  `governance/ai-build-review-checklist.md`, and the review still fills in the whole checklist top to
  bottom. This file sorts one group of those lines by how they get answered, so the ones a run cannot
  settle get opened instead of assumed.
- The adversarial-run checks cannot be skipped either. The three-way split is not a ranking with the happy
  path safe at the bottom. The happy path is the weakest evidence of the three, because it shows the one
  case the build was made to handle. Idempotency, the error path, and the failure alert each need their own
  run, a bad input or a repeat, and a clean single run is silent on all three. Day 015's double-post is the
  cost of eyeballing one of those instead of running it. This file centers category 3 because a passing run
  there gives false reassurance, and the category-2 checks still demand their own runs.
- Opening the node is how you look. Finding the problem is a separate thing. This guardrail gets you to
  open the right thing and tells you what to open. It does not read it for you. On the secrets line you
  still have to recognize that a token in an authorization header is a token in a node parameter; on the
  scope line you still have to know that read access is enough for a build that only reads. Opening is the
  necessary first move. The judgment comes after it.

## Where this sits and what it cannot do

This is the exact blind spot the review spot-audit (`governance/review-spot-audit.md`) and the review miss
rate (`analytics/metric-definitions.md`) exist for. A category-3 line marked passing off a clean run,
without the node opened, looks identical to one that was actually inspected, because the build runs the
same either way and so does the checklist mark. The spot-audit re-reviews a sample of approved builds cold
and actually opens the node, and the review miss rate is the number that finally counts the miss the
send-back rate scored as clean. Day 022 walks that whole catch: the false approval the send-back rate read
as a clean zero, the audit that opened the node the review never opened, and the token in the header.

A skipped inspection is a real gap, in the sense `enablement/handling-a-review-miss.md` gives the term: a
check marked passed without being run, where running it would have caught the problem. It is not a judgment
call, because section 5 and the checklist line are plain. The fix is a habit, one you can say in a
sentence: on these lines, open the thing and look, and do not read the fact that the build works as the
answer.

Here is the honest ceiling. A guardrail can name the checks that demand opening something. It cannot make
anyone open them. The same reasoning that marked Day 022's secrets line yes off a working build is
available on every line here, and a reviewer in a hurry can take it. What this file changes is that the
lines where that reasoning fails are now written down and labeled: a yes on one of them without an open
node is a yes with nothing behind it. The audit is what makes that skip detectable after the fact. Naming
the check is what makes the skip visible in the first place.

---

*v1. A living guardrail. It sorts the review checklist by what answers each line, so the checks only an
open node, credential, or register can settle stop getting marked off a clean run. The next pass turns each
inspection check into a one-line "what to open" a reviewer can run down the margin of the checklist, and
tests it against a second worked example whose flaw is an over-scoped key rather than a secret in a node.*
