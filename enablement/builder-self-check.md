# Builder Self-Check Before Handoff (v1)

You built something and it works on your machine. Before you hand it off for review, there is
prep only you can do. A reviewer can run your build and read your description, but they cannot
write that description, name the owner, or set up the rollback for you. This guide is that prep:
what to self-check and prepare so the review is a quick confirmation instead of a long
back-and-forth. Done right, the build reaches the reviewer already review-ready: an owner is
named, there is a rollback plan, and it has been run against both a good and a bad input.

It is the builder's side of `governance/ai-build-review-checklist.md`. Same quality bar, your
side of it. The reviewer walks that list; this list is how you get every item to a "yes" before
they open your build.

## 1. Run it yourself first

Do not hand off something you have only watched work once.

- [ ] Run the happy path end to end with a real-shaped sample input. Confirm it does what your description will claim.
- [ ] Run a failure case on purpose. Feed it bad input or a call that should fail, and watch where it lands. A build with no answer for bad input is not finished, however clean the happy path looks.
- [ ] Confirm there is an error path, and that a person gets told when something fails, with enough detail to act: the build name, the failing input, the error, and a timestamp.
- [ ] Confirm expected failures (a 404 from a lookup) are handled in your logic, and only the unexpected ones (a 500, a timeout) raise an alert.
- [ ] Run the same input twice and confirm you do not get two of anything.

The reviewer runs the happy path and failure case too (see `sops/run-a-build-review.md`). If you
have run them first, there are no surprises left for them to find.

## 2. Make it safe to run

- [ ] Put every secret in the credential store, not typed into a step or sitting in the code.
- [ ] Use separate test and prod credentials, reuse nothing across environments, and suffix the environment on each.
- [ ] Scope each key to only what this build needs, nothing more.
- [ ] Confirm retries sit only on steps that are safe to run again, are capped and spaced out, and a run that exhausts them lands on the error path.

## 3. Make it operable by someone else

This is the part a reviewer cannot do for you. It covers section 8 (Ownership) and section 9
(Change and rollback) of `standards/automation-standards.md`. A build with no owner is a future
outage with nobody to call.

- [ ] Name one owner and record it next to the build or in a register. Not "the team." One person.
- [ ] Set up the rollback plan: a versioned, revertible definition (so you can see what changed and go back to a known-good version) plus a safe stop (a disable switch or flag that halts it cleanly, without leaving half-finished work).
- [ ] Point the build's alerts at a place a person actually reads, not a channel nobody opens.
- [ ] Confirm volume (how often it runs) and exception rate are tracked. Exception rate is the share of runs that errored or fell out to a person, defined in `analytics/metric-definitions.md`.

## 4. If your build calls a model

Skip this whole group if there is no model call.

- [ ] Confirm the output is checked before anything acts on it.
- [ ] Confirm a person is in the loop wherever the stakes are real.
- [ ] Confirm no private or sensitive data is going to the model that should not (a customer's full record when the model only needs the order id).
- [ ] Read your prompt against the job and confirm it asks for what you actually need.

## 5. Make it legible

- [ ] Write the one-paragraph "what this does and why." Without it the reviewer has no goal to check against, and it is the most common send-back.
- [ ] Mark any non-obvious decision with a sticky note or inline comment, so the reviewer does not have to guess why a step is there.
- [ ] If it will run in production, write an SOP someone else could follow and file it in `sops/`.

When all of these are true, hand it off; a clean self-check is what turns the review into a quick
confirmation instead of a long back-and-forth.

## What self-check does not replace

Self-check is preparation, not a substitute for a second reviewer. You are close to the build, so
you read past gaps you already know how to work around: the input you never thought to try, the
assumption you baked in and forgot, the step that is obvious only to you. That blindness is the
reason review exists. The point of this list is to clear the obvious problems yourself, so the
reviewer can spend their pass on the ones you cannot see. A clean self-check makes review fast. It
does not make it optional.

---

*v1. A living guide. Each pass tightens a step or adds one once a real handoff showed where a
builder and a reviewer still went back and forth.*
