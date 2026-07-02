# SOP: Hand Off a Build for Review (v1)

**Purpose:** move a finished build from the person who built it to the person who reviews it, and
move the decision back, along one documented path, so nothing gets lost in the handoff and a
send-back returns the same way it went out.

**When to use this:** any time a shared or production-bound build is done and needs sign-off, from
the moment the builder thinks it is ready to the moment a decision is returned.

**Who runs it:** two roles, one on each side of a single handoff point. The builder prepares the
build and hands it off. The reviewer takes it, reviews it, and sends the decision back. This SOP is
the glue between them; it does not replace the guide each role runs on its own side.

## Before you start

The builder needs:

- A build that runs, not a screenshot or a plan for one.
- The self-check done: `enablement/builder-self-check.md`. That guide is the builder's prep. Run it
  first.

The reviewer needs:

- The reviewer SOP open: `sops/run-a-build-review.md`. The reviewer runs this after handoff.
- The review checklist open: `governance/ai-build-review-checklist.md`. This is the message that
  comes back.

The packet is what enforces both sides. See "The handoff packet" below for what makes it complete.

## The handoff packet

The handoff packet is the set of things that travel across the handoff point from builder to
reviewer. It is the minimum a reviewer needs to start, and it is the whole message. If a piece is
missing, the handoff is not ready and the reviewer cannot start. The packet is:

- The runnable build itself, in a form the reviewer can open and run.
- A one-paragraph description: what this does and why.
- A confirmation that the self-check in `enablement/builder-self-check.md` is clean, including that
  the build was run against one good and one failing input, with an owner named and a rollback plan
  in place.

The builder cannot assemble this packet without a clean self-check, since the self-check is what
produces the description, the owner, the rollback, and the two runs. A reviewer who opens an
incomplete packet and finds no runnable build or no description sends it straight back, because the
reviewer SOP cannot start without both.

## Steps

1. **Finish the self-check.** The builder runs `enablement/builder-self-check.md` top to bottom and
   gets every item to a "yes." Do not copy those items here, run that guide. This is the step a
   send-back re-enters at.

2. **Assemble the packet.** Gather the three things listed under "The handoff packet": the runnable
   build, the one-paragraph description, and the confirmation that the self-check is clean with an
   owner and a rollback in place.

3. **Hand it off.** Send the complete packet to the reviewer. This is the handoff point. Before this
   line the build is the builder's; after it, the reviewer drives, and the builder waits for the
   decision. Do not hand off a partial packet and promise the rest later. A partial packet is not a
   handoff.

4. **Run the review.** The reviewer runs `sops/run-a-build-review.md` against the build, start to
   finish, filling in `governance/ai-build-review-checklist.md`. Do not copy those steps here, run
   that SOP. It lands on exactly one of three outcomes: Approve, Approve with fixes, or Send back.

5. **Return the decision.** The reviewer sends the filled-in checklist back to the builder. The
   filled-in checklist is the message that comes back. It carries the decision and the reasons, so
   nothing has to be re-explained.

6. **Close the loop.** The builder reads the returned checklist and acts on the outcome (see the
   next section). If the build was sent back, the reasons in the checklist are the to-do list, and
   the build re-enters at step 1 when it returns.

## What each outcome means

The review lands on exactly one of three outcomes, all carried in the returned checklist:

- **Approve:** the build ships as is. File the checklist with it. The path ends.
- **Approve with fixes:** the build ships once the listed fixes are done. The builder makes the
  fixes and confirms them; a small fix does not need a second full trip through this path. The path
  ends.
- **Send back:** the build is not ready. This is not a dead end. The reasons in the checklist are
  the to-do list. The builder addresses them, re-runs the self-check, rebuilds the packet, and hands
  off again at step 3. The same path carries it back out.

A send-back does not start a new, separate process. It re-enters this one. That is why the path is a
loop and not a line: the build can go around it more than once, and each trip uses the same handoff
point and the same packet.

## Where this fits

Three documents, one loop. The self-check is the builder's side of the quality bar. The reviewer SOP
is the reviewer's side of the same bar. The filled checklist is what travels back down the path with
the decision. When all three agree, a build goes from done to decided the same way every time, and a
send-back has an obvious way home.

---

*v1. A living SOP. When a real handoff drops something between the two roles, name it in the packet
here so the next one does not.*
