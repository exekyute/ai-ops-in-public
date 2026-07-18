# Automation Standards (v2)

The difference between an automation that demos well and one a team can depend on is almost
entirely convention. This is the baseline every workflow in a shared environment should meet.
It is tool-agnostic; the examples lean on n8n but the rules apply to any orchestrator.

v2 deepens v1: every core section now has a short "what good looks like" line, and two areas a
real program cannot skip have been added, ownership and change/rollback. The changes are listed
at the end. For these rules in practice, `examples/` traces two synthetic builds through them:
one whose only flaw is a failed section 4 (idempotency) that the review catches, and one that
runs clean while breaking section 5 (secrets and access) in a way only inspection finds.

## 1. Naming

A name should tell the next person what runs, what it touches, and how often, without opening it.

- **Workflows:** `<domain>-<trigger>-<action>`, e.g. `intake-webhook-route-to-vendor`.
- **Nodes:** verb-first and specific: `Validate payload`, not `Function`, `Code1`, `IF`.
- **Credentials:** `<service>-<scope>-<env>`, e.g. `slack-notifications-prod`.
- **Environments:** never reuse one credential across test and prod. Suffix everything.
- *What good looks like:* you can scan a list of twenty workflows and know what each one does and
  what it touches, without opening a single one.

## 2. Error handling

Silent failure is the most expensive bug in operations, because nobody knows it happened.

- Every workflow that runs unattended has an **error path**, not only a happy path.
- Trigger and external-call nodes set an explicit `onError` behavior. Default to surfacing, not
  swallowing.
- A failure notifies a human channel with: workflow name, the input that failed, the error
  message, and a timestamp. Enough to triage without opening logs.
- Distinguish **expected** failures (a 404 from a lookup) from **unexpected** ones (a 500, a
  timeout). Handle the first in logic; alert on the second.
- *What good looks like:* the first person to know a run failed is you, from an alert, not the
  business three days later asking where their report went.

## 3. Retries and backoff

- Retry only **idempotent** steps (see below). Retrying a non-idempotent write doubles the side
  effect.
- Cap retries (3 is a sane default) and use backoff, not a tight loop, so you do not hammer a
  struggling dependency.
- After the cap, route to the error path. A retry budget is not an excuse to never fail.

## 4. Idempotency

Running the same input twice should not create two of anything.

- Key writes on a stable identifier (an order id, an email, a hash of the payload).
- Prefer **upsert** over blind insert. Check-then-write where upsert is not available.
- For outbound messages, dedup on a content key within a time window so a re-run does not
  double-notify.
- *What good looks like:* you can safely re-run yesterday's failed batch without anyone getting a
  second invoice or a duplicate ticket.

## 5. Secrets and access

- Secrets live in the credential store, never in node parameters, code, or commit history.
- Scope tokens to the minimum the workflow needs. A workflow that reads a sheet does not need
  write access.
- Rotate on a schedule and on any suspected exposure. Document where each credential is used.

## 6. Observability

- Log the start, the decision branches taken, and the end state of each run.
- Capture enough to answer "what did this do, to what, and when" after the fact.
- Track at least one volume metric (runs per day) and one health metric (exception rate, defined
  in `analytics/metric-definitions.md`) per workflow.

## 7. Documentation that travels with the build

- Every shared workflow has a one-paragraph description: what it does and, more importantly,
  *why* it exists.
- Sticky notes or inline comments mark any non-obvious decision.
- A workflow that matters enough to run in production matters enough to have an SOP in `sops/`.

## 8. Ownership

A shared automation with no owner is a future outage with nobody to call.

- Every workflow that runs in production names one owner, accountable for it, recorded next to
  the build or in a simple register.
- The owner is responsible for three things: that the alerts go to a place a person reads, that
  the metric gets looked at on a set cadence, and that the credentials get rotated.
- When the owner changes role or leaves, the handover is explicit. Ownership does not lapse by
  default.
- *What good looks like:* when a build starts failing at 8am, there is no question about whose job
  it is to look.

## 9. Change and rollback

A live automation will need to change, and some changes will be wrong. Plan for both.

- Workflow definitions are versioned, so you can see what changed and revert to a known-good
  version. Export to the repo or use the tool's version history. Do not edit production blind.
- Every production workflow has a safe way to stop it: a disable switch or a flag that halts it
  cleanly without leaving half-finished work behind.
- Test a change against sample input before it touches real data. "It validated" is not "it ran."
- *What good looks like:* a bad change can be backed out in minutes, not rebuilt from memory.

## What changed in v2

- Added section 8 (Ownership) and section 9 (Change and rollback), the two gaps the week 1
  integration map flagged as missing from the loop.
- Added a "what good looks like" line to naming, error handling, idempotency, ownership, and
  change/rollback, so each rule has a visible pass condition.
- Pointed the observability health metric at the exception rate definition shipped on Day 005, so
  the standard and the analytics side name the same number.

---

*v2. A living standard. The next pass turns the credential and ownership registers into real
templates, and adds a worked example workflow that meets every rule.*
