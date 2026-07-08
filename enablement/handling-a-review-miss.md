# Handling a Review Miss (v1)

The spot-audit (`governance/review-spot-audit.md`) turns up misses: a place where a second review of the
same build disagreed with the first. Finding the miss is all the audit can do. A miss is worth something
only if the conversation after it makes the next review sharper. Delivered as a charge ("you approved a
bad build"), it does the opposite: the reviewer gets defensive and protects themselves instead of judging
builds. The audit doc already says to treat a miss as a conversation and not a charge, and it stops there;
this guide is the how.

## Why the conversation is the point

The audit produces a note: this build, its original outcome, the audit outcome, and the one check that
split them. On its own that note changes nothing. Nobody reviews differently because a miss got written
down. The outcome the audit is actually after is the reviewer adjusting how they review, and that only
happens in the conversation.

That conversation is fragile. The reviewer is the person whose call got second-guessed, so the default
read is a judgment on them. Once it reads that way, they defend the call instead of examining it, and you
learn nothing about the next review. Everything below is about keeping the conversation on the build and
off the person, because that is the only version of it that pays.

## The two kinds of miss

Before anyone talks about a fix, say which kind of miss this is, and say it together. There are two, and
they are handled differently.

**A judgment call.** The standard genuinely leaves room, and two careful reviewers read the same build
differently. This shows up most on the line between approve-with-fixes and send-back, where the same gap
can honestly read either way. Nobody was wrong here. The standard was a shade ambiguous, and the
conversation settles where the line sits, so it is a shade less ambiguous next time.

**A real gap.** The reviewer marked a check as passed without running it, and running it would have caught
the problem. The worked example (`examples/a-build-through-the-loop.md`) shows the mechanic cleanly,
though there it is the builder who eyeballs the idempotency item ("running the same input twice does not
create two of anything") and the reviewer who catches the double-post by running the day twice. The
example's own closing names the miss you are handling here: had the reviewer eyeballed that same item, the
second identical reminder would have shipped. That is the real gap, a check read instead of run. The
conversation is short: here is the check, here is what running it shows, run it next time. The fix is a
habit, not a scolding.

Getting the kind wrong is how the conversation goes sideways. Treat a judgment call as a real gap and you
are telling someone off for a call the standard allowed. Treat a real gap as a judgment call and the habit
that caused it never changes. Naming the kind together, out loud, is the first move, and it is most of the
de-escalation.

## How to run it

Keep it short, and keep it on the build.

1. **Start from the build, not the reviewer.** Open with "two reviews of this build landed differently,
   let us work out the right call," rather than "you missed this." The first sentence sets whether this is
   a shared problem or an accusation, and you do not get it back.

2. **Settle the right call against the standard.** Put the build next to `standards/automation-standards.md`,
   find the check that split you in `governance/ai-build-review-checklist.md`, and work out which reading
   the standard actually supports. The standard is the third party in the room, so the answer comes from
   it, not from whose word carries more weight. This step has to be able to end with the audit being the
   one that got it wrong.

3. **Name the kind, together.** Judgment call or real gap, decided out loud. This is the move most
   conversations skip, and skipping it is why they curdle. A real gap named plainly ("that check got read,
   not run") is easier to accept than one left implied.

4. **Agree the smallest change that closes it.** For a judgment call, that is one line: where the
   approve-with-fixes and send-back split sits for this kind of build, so the next two reviewers land
   together. One such line stays a light note. The same line coming back a second time is the cue to push
   the call up into `standards/automation-standards.md` or `governance/ai-build-review-checklist.md`, where
   every reviewer inherits it instead of two people resettling it each time. For a real gap, the change is
   one habit: that check gets run, not eyeballed. Small enough to say in a sentence and remember next week.

5. **Keep the record light and shared.** The output is a one-line "what changes next time," somewhere both
   people can see it, not a file in the reviewer's folder. A miss logged into someone's personal record
   turns into evidence, and the next section is what that does.

## What kills it

Each of these turns the reviewer defensive, and a defensive reviewer stops judging builds.

- **A miss delivered as a verdict.** "You approved a bad build" leaves the reviewer one rational move: stop
  making calls that can be traced to them. They rubber-stamp harder so nothing is their fault, or they send
  everything back so nothing they touched can be a false approval. Either way the review stops meaning
  anything, which is the exact rubber stamp the audit was built to catch. The miss has to arrive as a
  question about the build, every time.

- **The auditor treated as infallible.** The auditor has to be able to lose the argument. Sometimes the
  audit is the one that got the call wrong, which the spot-audit doc says plainly. If the audit is right by
  definition, it is a second rubber stamp carrying more authority than the first, and the reviewer learns
  their job is to agree with the auditor rather than to read the build. When the standard's reading favors
  the original reviewer, the miss belongs to the audit, and you say so. The auditor is auditable too, which
  is what the rotation in the spot-audit doc is for.

- **Counting misses as a scoreboard.** The moment a miss is ammunition, honesty leaves the room. A reviewer
  who is being kept score against optimizes the count instead of the reviews: they stop surfacing their own
  close calls, argue every miss instead of learning from it, and drift toward whichever decision is safest
  to defend. A single miss is a note, not a tally. This sits on a different axis from the pattern the
  spot-audit doc describes: a pattern is one reviewer's approvals coming back as misses on checks that are
  not close calls, read by hand across audits, which is a real signal and still not a running score held
  over someone.

## Limits

Be honest about what this guide can and cannot do.

- A guide cannot manufacture good faith. If the reviewer and the auditor do not both want sharper reviews,
  no opening line produces them, and the conversation becomes a negotiation over blame. The words help only
  where the intent behind them is real.
- The audit only works where a miss can be a calibration without being a threat. Where any admitted miss
  becomes a mark on a record, the rational reviewer stops admitting them, and the audit goes blind. Fix
  that condition first, because the conversation cannot carry it alone.
- The first miss conversation is the real test. Everyone can agree in the abstract that a miss is a
  calibration. The first time a specific reviewer's specific approval comes back as a miss, the room finds
  out whether that was true. Handle the first one as a shared problem about a build and the ones after it
  get easier. Handle it as a charge and every reviewer watching learns to protect themselves, and no later
  guide undoes that.

---

*v1. A living guide. The next pass adds the openings and phrasings that held once a real miss conversation
showed which ones kept it a calibration and which tipped it into a defense.*
