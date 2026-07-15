# AI Build Review Checklist (v2)

Run this against a submitted automation before it goes live. The goal is that two different
people running this list land on the same decision. If a check needs a paragraph to explain,
split it in two.

This is the checklist that enforces `standards/automation-standards.md`. The standard is now v2
and added two sections, ownership and change/rollback, so this checklist adds the matching checks.
When the standard moves, this file moves with it.

Mark each one: yes / no / not applicable.

## Basics

These come from the automation standards. Any "no" here is a fix before approval.

- [ ] The name says what it does, so you can tell from the list without opening it.
- [ ] Nodes and steps are named for what they do, not left as defaults.
- [ ] Test and prod use separate credentials. Nothing is reused across environments, and the env is suffixed on every credential.
- [ ] There is an error path, not only a happy path.
- [ ] When something fails, a person gets told, with enough detail to act on.
- [ ] Expected failures (a 404 from a lookup) are handled in logic; only the unexpected ones (a 500, a timeout) raise an alert.
- [ ] Retries only happen on steps that are safe to run again.
- [ ] Retries are capped and spaced out, not a tight loop, and a run that exhausts them lands on the error path.
- [ ] Running the same input twice does not create two of anything.
- [ ] Secrets are in the credential store, not typed into a step or sitting in the code.
- [ ] Each key can only do what this build needs, nothing more.
- [ ] Credentials are rotated on a schedule, and where each one is used is written down.
- [ ] There is enough logging to answer "what did this do, to what, when, and which branch it took."
- [ ] The build tracks how often it runs (volume) and its exception rate (the share of runs that errored or fell out to a person, defined in `analytics/metric-definitions.md`).

## AI steps

Only for builds that call a model. Skip if there are none.

- [ ] The output is checked before anything acts on it.
- [ ] A person is in the loop wherever the stakes are real.
- [ ] No private or sensitive data is going somewhere it should not (this is the section 5 access scope applied to model calls).
- [ ] The prompt actually matches the job it is being asked to do.

## Ownership and lifecycle

These apply to anything that runs in production. Any "no" here is a fix before it goes live.

- [ ] One person is named as the owner, recorded next to the build or in a register.
- [ ] The alerts from this build go to a place a person actually reads, not a channel nobody opens.
- [ ] The health metric gets looked at on a set cadence, and someone is named to do it.
- [ ] The credentials this build uses have an owner and get rotated on a schedule.
- [ ] When the owner changes role or leaves, handover is explicit; ownership does not lapse by default.
- [ ] The workflow definition is versioned, so you can see what changed and revert to a known-good version. It is not edited in production blind.
- [ ] There is a safe way to stop it: a disable switch or flag that halts it cleanly, without leaving half-finished work.
- [ ] The change was run against sample input before it touched real data. Validation is not the same as a real run.

## Documentation

- [ ] There is a plain description of what the build does and why it exists.
- [ ] Any non-obvious decision is marked with a sticky note or inline comment.
- [ ] If it is going to run in production, it has an SOP someone else could follow.

## Decision

Pick one:

- [ ] **Approve.** Ships as is.
- [ ] **Approve with fixes.** Ships once the items below are done.
- [ ] **Send back.** Not ready. Reasons below.

Fixes or reasons:

1.
2.
3.

## What changed in v2

- Added an "Ownership and lifecycle" section for the standard's section 8 (Ownership): a named owner recorded, alerts read by a person, the metric looked at on a cadence, credentials rotated, and explicit handover when the owner changes.
- Same section adds the standard's section 9 (Change and rollback): a versioned and revertible definition, a safe stop, and a change tested on sample input before real data.
- Added the Basics checks the v1 had skipped: separate test/prod credentials with an env suffix, scheduled rotation with credential usage documented, the run-volume and exception-rate metric, and a sticky-note/inline-comment check in Documentation.
- Split two Basics checks that were doing double work: retries now also check the cap and backoff, and error handling now separates expected failures, handled in logic, from unexpected ones, which alert. The logging check now also asks which branch a run took.

---

*v2. A living checklist. It now checks the two standard rules a week of use turned up, a named owner and a safe rollback, plus the Basics rules the v1 had skipped. The next pass folds in a worked example so a reviewer can see a passing build, not only the questions.*
