# AI Build Review Checklist (v1)

Run this against a submitted automation before it goes live. The goal is that two different
people running this list land on the same decision. If a check needs a paragraph to explain,
it is probably two checks.

Mark each one: yes / no / not applicable.

## Basics

These come from the automation standards. Any "no" here is a fix before approval.

- [ ] The name says what it does, so you can tell from the list without opening it.
- [ ] Nodes and steps are named for what they do, not left as defaults.
- [ ] There is an error path, not just a happy path.
- [ ] When something fails, a person gets told, with enough detail to act on.
- [ ] Retries only happen on steps that are safe to run again.
- [ ] Running the same input twice does not create two of anything.
- [ ] Secrets are in the credential store, not typed into a step or sitting in the code.
- [ ] Each key can only do what this build needs, nothing more.
- [ ] There is enough logging to answer "what did this do, to what, and when."

## AI steps

Only for builds that call a model. Skip if there are none.

- [ ] The output is checked before anything acts on it.
- [ ] A person is in the loop wherever the stakes are real.
- [ ] No private or sensitive data is going somewhere it should not.
- [ ] The prompt actually matches the job it is being asked to do.

## Documentation

- [ ] There is a plain description of what the build does and why it exists.
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

---

*v1. A living checklist. Each later pass tightens a check or adds one a real review turned up.*
