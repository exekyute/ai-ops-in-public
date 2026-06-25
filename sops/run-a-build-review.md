# SOP: Run a Build Review (v1)

**Purpose:** take a submitted automation from "someone says it is done" to a clear decision,
the same way every time, so the result does not depend on who reviewed it.

**When to use this:** any time a shared or production-bound automation is handed over for
sign-off, before it goes live.

**Who runs it:** anyone doing the review. You do not need to have built the thing. That is
the point.

## Before you start

You need:

- Access to the build itself, not a screenshot or a description of it.
- A sample input you can run through it, ideally one real-shaped case and one that should
  fail.
- The review checklist open: `governance/ai-build-review-checklist.md`.
- The standards on hand for reference: `standards/automation-standards.md`.

If you are missing the build or a way to run it, stop. Send it back for those first. You
cannot review what you cannot see run.

## Steps

1. **Read the description.** Find the one-paragraph "what this does and why." If there is no
   description, that is your first send-back. You cannot judge a build against a goal you
   have to guess.

2. **Run the happy path.** Put the good sample input through it. Confirm it does the thing
   the description claims, end to end.

3. **Run the failure case.** Put the bad input through it. Watch what happens. A build that
   has no answer for bad input is not finished, no matter how clean the happy path looks.

4. **Walk the checklist, top to bottom.** Mark each item yes, no, or not applicable. Do not
   skip ahead. If an item needs a paragraph of explaining, note it and move on.

5. **Handle the AI section only if the build calls a model.** If it does not, mark those
   items not applicable and keep going.

6. **Land on a decision.** Use the marks, not your gut:
   - All checks pass: **Approve.**
   - Passes except for small, clearly listed fixes: **Approve with fixes.** Write the fixes
     in the checklist.
   - Any basic check fails, or the build does not do what the description says: **Send back.**
     Write the reasons.

7. **Send the result back to the builder.** The filled-in checklist is the message. It says
   what you decided and why, so there is nothing to re-explain later.

## What each outcome means

- **Approve:** the build ships as is. File the checklist with it.
- **Approve with fixes:** the build ships once the listed fixes are done. The builder does
  not need a second full review for small fixes, only a confirmation they happened.
- **Send back:** the build is not ready. The reasons you wrote are the to-do list. It comes
  back through this same SOP when it returns.

## Common send-back reasons

These come up most often. Check for them early to save a full pass:

- No description, so there is no goal to review against.
- Happy path only, nothing handles bad input or a failed call.
- A retry sits on a step that is not safe to run twice.
- Secrets typed into a node instead of the credential store.
- No way for a human to find out when it fails.

---

*v1. A living SOP. When a review turns up a step this missed, add it here.*
