# Prompt and Model Change Control (v1)

Someone rewrites two sentences of a prompt in a text box to fix a case the model kept getting wrong, and saves. From the next run on, the build decides differently, with no diff, no version, no author, and nothing for anyone to review. [The automation standard](automation-standards.md), the baseline every build in this repo is judged against, already forbids that in its section 9: definitions are versioned so you can see what changed and revert to a known-good version, and you do not edit production blind. That rule was written for a workflow definition, a thing you can export and diff. A prompt is a string in a parameter field, so the same edit breaks the same rule and does not feel like it. The model id, the decoding parameters, the tools the model can call, and the shape of the output all have the problem, and some of them change with no author at all.

These rules are tool-agnostic; a model step in an orchestrator and one in code both take them. A bare "section N" means a section of this file, and the standard's own sections are always named as such.

## 1. What is under control

Six things make up a model step's configuration. Every one of them changes what the build decides, so treat them as one unit.

- **Prompt text:** the system instruction, the task instruction, the examples, the formatting rules, and any template that assembles them.
- **Model id and version:** exactly as sent to the provider, including a move between sizes of the same family.
- **Decoding parameters:** temperature, top-p, max tokens, stop sequences, and the seed if you set one.
- **Tool or function definitions:** the tools the model can call, including their descriptions. A tool description is instruction text the model reads.
- **Output schema:** the fields, the types, the allowed values in an enum, plus any parser or validator applied to it.
- **Grounding or retrieval source:** if the step has one, which corpus, which index, how much comes back.
- "I only swapped the model" and "I only added an example" are both changes to this list. One kind of change, one procedure.
- *What good looks like:* one place holds all six items, and you can say which version of each was live on a given date.

The recorded placement is not on this list. It is the claim those six were judged against, which is why any change to them re-opens it (section 4).

## 2. Pin the version

A pinned version is what turns a provider-side change into an event somebody can review.

- Send an explicit, dated model version. Never an alias meaning "latest" or "the current one," however convenient it reads.
- Pin the decoding parameters too. A default you never set is a value the provider chose and can change.
- Store the exact prompt text. The name of a prompt does not identify a version.
- Record the pinned ids where the build's owner is recorded. Section 8 of the standard already puts an owner next to the build or in a register; the configuration goes in the same place.
- Test and prod point at the same pinned version, or the test result describes a different model than the one that runs.
- A pinned id fixes what you send, not what the provider serves. Serving stacks and safety filters move behind a stable id, so re-run the input set in section 6 on a set cadence, not only when you change something.
- Where something cannot be pinned, write down what you could not pin, so nobody later reads a pinned id as a guarantee about the whole step.
- *What good looks like:* two people can say which model version ran last Tuesday, and they agree.

## 3. Changes nobody made

Two things move a model step with nobody touching it. A floating alias is the `latest` tag problem, and the fix is the one you already use on dependencies. What differs is that a library change shows up as a diff, and a model change shows up as prose that still parses.

- **Alias drift.** A floating alias repoints under you: no edit, no commit, no author, no event to review. Pinning is the whole defense.
- **Retirement.** A pin buys notice, not permanence. So name one person to watch the provider's deprecation notices and put the retirement dates on a calendar the build's owner reads. That person is the owner under section 8 of the standard unless somebody else is written down.
- Take a forced migration on your own schedule, ahead of the deadline, as a change you are making. It goes through section 5 like any other, and it lands while the old version still runs so you have something to compare against.
- Do not let the retirement date pick the day. A migration done on the deadline is an unreviewed change with no fallback.
- *What good looks like:* on the day the old version goes dark, you moved weeks earlier, on a date you chose, and the move was reviewed.

## 4. The placement is a claim about a version

[Where a human stays in the loop](../enablement/where-a-human-stays-in-the-loop.md), the guide that decides where a person reads model output, asks two design-time questions whose answers pick a **placement**, written in one line next to the build. Both answers describe this prompt and this model.

- The recorded line names the pinned model version and the prompt version the placement was decided against. A placement with no version on it describes a build that may no longer exist.
- Any change in section 1 re-opens it. Re-answer both questions, then write a new line or record that the answers did not move. Usually they do not, and recording that is the whole cost.
- Look hardest at changes to the output schema and the tool definitions. Both change what a wrong output can look like and what would catch it.
- *What good looks like:* the placement line and the configuration line name the same version, written on the same day.

## 5. Review a change like a build

A configuration change is a handoff. It preps against [the builder self-check](../enablement/builder-self-check.md), travels the path in [the handoff SOP](../sops/hand-off-a-build-for-review.md), and is decided on [the review checklist](../governance/ai-build-review-checklist.md), the list a build passes before it goes live. Sending all 29 boxes back for a two-line prompt edit is how a rule gets ignored, so name the subset.

Two of the lines below are edits the checklist has not taken yet. The placement declaration becomes a line under AI steps, and the versioned-and-revertible line widens from the workflow definition to the configuration in section 1. Until both land, a reviewer checks them off this file.

Re-opens on any change in section 1:

- The four AI-steps lines: the output is checked before anything acts on it, a person is in the loop wherever the stakes are real, no sensitive data goes where it should not, and the prompt matches the job.
- The placement recorded next to the build (section 4), which is what settles that stakes line, so read the declaration rather than re-guessing the stakes.
- The versioned-and-revertible line, now covering the configuration as well as the definition (section 7).
- The sample-input line, which section 6 rewrites for a model step.
- The safe-stop line (section 7).

Three changes reach further. A change that lets the model call a tool, or that adds a field to what the model is sent, re-opens access scope and, if that step writes anything, retries and idempotency. A change to text that a deduplication key is computed from re-opens idempotency too, because the key moves and a re-run double-sends. A change to what the step decides, rather than how well it decides it, re-opens the plain description and the SOP, because both now describe a build that does something else.

Nothing else re-opens unless the change touched it. Naming, secrets, ownership, alert routing, and logging all stand. A reworded prompt does not change who owns the build.

- On these lines a run is no evidence, because a build whose prompt matches the job and one whose prompt does not both finish green. The reviewer opens the step and reads the configuration and the payload. That is the move in [the inspection-required checks](../governance/inspection-required-checks.md), the file that sorts checklist lines by what can answer each, where the sensitive-data and versioned-and-revertible lines are already classified.
- The packet names every item that changed, with the old value, the new value, why, and the evidence from section 6. "I tweaked the prompt" is not a packet.
- *What good looks like:* a reviewer opens the packet, walks the named lines, and can say which of them the change touched, without re-running the whole list.

## 6. One run is not a test

Section 9 of the standard says test a change against sample input before it touches real data, and "it validated" is not "it ran." The input you tested is not the input that arrives tomorrow, so one run tells you about one input. Pinning temperature and the seed narrows the spread without closing it, because hosted inference is not reproducible call to call.

- Run the old configuration and the new one against the same set of inputs, or the comparison says nothing.
- Put the case that prompted the change in the set, along with the cases this build has gotten wrong before. A set of easy inputs agrees with every change you make.
- A clean workflow run settles the happy path and nothing else. A model step adds a second failure: the path can be right while the output is wrong.
- Until the set is defined, write in the packet what you actually ran against and how many cases. "Five inputs, all read by hand" beats "tested."
- *What good looks like:* you can say the new prompt ran on the same 40 inputs as the old one, and here are the 3 that changed.

## 7. Rollback

For a workflow you revert the definition. For a model step you restore the previous configuration, and you can only restore what you kept.

- Keep the previous configuration wherever the definition already gets versioned: the export in the repo, or the tool's version history. Where the tool offers neither, paste the current prompt text and the pinned ids into a file you version before you touch the box.
- Previous means every item in section 1, restored together. A partial restore is a new configuration nobody reviewed, and it reads like a rollback.
- Where the old prompt lives only in the memory of whoever edited the box, there is no rollback, only a rewrite done under pressure. The standard's section 9 safe stop is then all you have: a switch that halts the build cleanly.
- Output quality dropping is a trigger on its own, since a model step that quietly got worse raises nothing.
- A rollback is itself a change. It goes back through section 5 at whatever speed the incident allows, and it gets recorded like any other.
- You cannot roll back to a retired version. That is the situation section 3's migration schedule exists to prevent.
- *What good looks like:* yesterday's configuration goes back in one action, and you can prove it is yesterday's.

## What this does not cover

- Whether a change is a good idea. This governs how a change gets made, reviewed, and undone, not whether the new prompt is better than the old one.
- Fine-tuned and self-hosted models, which add version questions about training data and weights. Everything above still applies to the configuration around them.
- Providers differ in what they expose, and some endpoints have no version to pin at all. Section 2 says record that, so an uncontrolled step is visible as one.

A model step's behavior traces back to a version somebody chose. Pin it, and every change to that step gets an author, a date, a review, and a way back, including the drift and the retirements the provider hands you.

---

*v1. A living standard. The next pass names the set of inputs a prompt change has to clear and the threshold that clears it, and runs a model swap through all seven rules end to end.*
