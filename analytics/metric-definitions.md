# Metric Definitions (v1)

A number is only useful if everyone reading it counts the same thing. This file defines the
metrics this lab uses to tell whether an automation is actually working, one entry at a time.
Each entry pins down what the metric is, the exact formula, what counts and what does not,
where the data comes from, how often to read it, and the ways the number can mislead you.

The rule for adding a metric here: if you cannot compute it by hand from a sample of run logs,
it is not defined well enough to belong yet. All examples use synthetic data.

## Exception rate

**What it is.** Of all the times an automation ran in a period, the share that did not finish
on their own. An exception is any run that ended in an error, or that had to be handed to a
person to decide or fix before it could complete. The rest are straight through: started,
finished, no human needed.

**Why it matters.** It is the most honest health signal an automation has. A workflow can look
impressive and still be mostly manual underneath. If one run in three falls out to a person,
the automation is doing less of the work than the demo suggested, and you want to know that
before you call it done.

**Formula.**

    exception rate = exceptions / total runs

**What counts.**

- *Total runs* is every run started in the period, including the ones that failed. Count
  attempts, not just successes, or the rate will flatter you.
- *Exceptions* is a run that either ended in an error state, or was routed to a person to
  resolve. Decide per workflow what "routed to a person" means and write it down next to the
  build, so the count does not drift over time.
- A run that retried on its own and then finished is not an exception. The point is whether a
  human had to step in, not whether the first attempt was clean.

**Where the data comes from.** The execution or run log of the tool itself. You need, at a
minimum, one row per run with a final status and a timestamp. If the log cannot tell you
whether a run finished on its own, that is the first thing to fix, because nothing here is
measurable until it can.

**How often to read it.** Weekly per workflow is enough to see a trend without chasing noise.

**How to read it without fooling yourself.**

- *Watch the volume.* A 30 percent rate on 10 runs is one bad afternoon, not a pattern. Put the
  run count next to the rate, every time.
- *Segment by reason.* A single rate hides the cause. The fix for "the input was malformed" is
  not the fix for "the model's answer needed a human check," and one number cannot tell them
  apart.
- *Mind the runs that never start.* A run that silently fails to trigger never lands in the
  log, so it never counts as an exception. A falling rate can mean the work is getting cleaner,
  or it can mean fewer runs are firing at all. Check the volume before you celebrate.

**A worked example (synthetic).** A weekly intake automation ran 120 times. 12 ended in errors,
and 18 were handed to a person to fix a field before they could continue. Exceptions are 30, so
the exception rate is 30 / 120, or 25 percent. Three in four ran straight through. Next to that
you would note the count (120) and the split (12 errors, 18 human fixes), because the 18 is
where the next improvement probably lives.

**On targets.** There is no universal good number. Set a threshold per workflow based on what
it does and what a fallout costs, then watch the trend more than the absolute value. A rate
that drifts up week over week is a problem even if it is still low.

---

*v1. A living dictionary. Each later pass adds a metric or sharpens one once a real read of the
data showed where it was vague.*
