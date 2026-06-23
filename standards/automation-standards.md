# Automation Standards (v1)

The difference between an automation that demos well and one a team can depend on is almost
entirely convention. This is the baseline every workflow in a shared environment should meet.
It is tool-agnostic; the examples lean on n8n but the rules apply to any orchestrator.

## 1. Naming

A name should tell the next person what runs, what it touches, and how often, without opening it.

- **Workflows:** `<domain>-<trigger>-<action>` , e.g. `intake-webhook-route-to-vendor`.
- **Nodes:** verb-first and specific: `Validate payload`, not `Function`, `Code1`, `IF`.
- **Credentials:** `<service>-<scope>-<env>`, e.g. `slack-notifications-prod`.
- **Environments:** never reuse one credential across test and prod. Suffix everything.

## 2. Error handling

Silent failure is the most expensive bug in operations, because nobody knows it happened.

- Every workflow that runs unattended has an **error path**, not just a happy path.
- Trigger and external-call nodes set an explicit `onError` behavior. Default to surfacing,
  not swallowing.
- A failure notifies a human channel with: workflow name, the input that failed, the error
  message, and a timestamp. Enough to triage without opening logs.
- Distinguish **expected** failures (a 404 from a lookup) from **unexpected** ones (a 500,
  a timeout). Handle the first in logic; alert on the second.

## 3. Retries and backoff

- Retry only **idempotent** steps (see below). Retrying a non-idempotent write doubles the
  side effect.
- Cap retries (3 is a sane default) and use backoff, not a tight loop, so you do not hammer
  a struggling dependency.
- After the cap, route to the error path. A retry budget is not an excuse to never fail.

## 4. Idempotency

Running the same input twice should not create two of anything.

- Key writes on a stable identifier (an order id, an email, a hash of the payload).
- Prefer **upsert** over blind insert. Check-then-write where upsert is not available.
- For outbound messages, dedup on a content key within a time window so a re-run does not
  double-notify.

## 5. Secrets and access

- Secrets live in the credential store, never in node parameters, code, or commit history.
- Scope tokens to the minimum the workflow needs. A workflow that reads a sheet does not
  need write access.
- Rotate on a schedule and on any suspected exposure. Document where each credential is used.

## 6. Observability

- Log the start, the decision branches taken, and the end state of each run.
- Capture enough to answer "what did this do, to what, and when" after the fact.
- Track at least one volume metric (runs/day) and one health metric (failure rate) per
  workflow. These feed the `analytics/` side of the repo.

## 7. Documentation traveling with the build

- Every shared workflow has a one-paragraph description: what it does and, more importantly,
  *why* it exists.
- Sticky notes or inline comments mark any non-obvious decision.
- A workflow that matters enough to run in production matters enough to have an SOP in
  `sops/`.

---

*v1. This is a living standard. Each later pass adds a worked example or tightens a rule.*
