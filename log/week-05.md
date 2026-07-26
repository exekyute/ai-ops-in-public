# Week 5 Log

Days 029 to 034. Week 1 was breadth, week 2 was depth, week 3 turned the loop on itself with an audit,
and week 4 scaled it to a pool of people. This week's job was to keep what those four weeks wrote.
Nothing new got designed: fill the records the earlier weeks had only described, settle the conflict the
rows exposed, put that ruling in front of whoever holds the pen, order a set that had grown past
browsing, decide how the whole thing gets checked, and map the five as one loop. Six days, six
artifacts, and the first week this repo maintained something instead of adding to it.

## What shipped

- `examples/a-populated-log-and-queue.md`: v1, the first records in this repo with rows instead of
  formulas, twelve handoffs and a four-build queue snapshot, with the three review-side metrics computed
  off real rows for the first time. Filling it took `sops/review-log-spec.md` to v2, adding a fifth
  required field, Handed off.
- `governance/what-counts-as-one-handoff.md`: v1, the ruling that settles the conflict the rows exposed.
  A handoff is one build's trip through review, the row the log keeps and the unit all three metrics
  count. An arrival is each entry into the queue, so one handoff can have several. Queue SOP to v2, log
  spec to v3.
- `enablement/keeping-the-review-log.md`: v1, the write-time habit for whoever keeps the log, four steps
  to run before any row goes down, built around one fail-safe: when you cannot tell whether a returning
  build is the same handoff, merge rather than split, because the undercount is the smaller error.
- `sops/the-review-loop-in-order.md`: v1, the index over seventeen review-side pieces, ordered by when
  you need them and grouped by role through the middle, so each reader takes one row and leaves the rest.
  It points and never summarizes, and it names its own failure mode, going stale silently.
- `analytics/measure-or-test.md`: v1, the memo answering the index's staleness claim with a check rather
  than a fifth metric, since the ground truth sits in the same directory. Measure what you must estimate,
  test what you can decide.
- `integration/week-05-the-loop-gets-kept.md`: v1, the five pieces mapped as one maintenance loop, the
  first of these maps whose feedback runs through editing, not a number.

## What I actually learned

I planned the shape of this week and none of its content. Day 028's reflect had named filling the
records as the week's first build. Filling them exposed a conflict, the conflict wanted a ruling, the
ruling wanted a place a person would meet it, and Friday's memo answered a staleness claim Thursday's
index had made about itself. Four days, each one taking up what the day before had made. The fifth, the
index, answered three weeks of accumulated volume that the day before had only sharpened. The pillar
slots were fixed in advance the way they are every week, Build then Govern then Enable then Document
then Analyze, and I knew on Sunday which day would be which. What I did not know was the subject that
would fill each slot. In weeks 2 through 4 that subject was a piece I chose because I had decided the
loop still needed it, a checklist because the review wanted a gate, a queue because builds pile up
behind one person. In week 5 it was whatever the day before had broken. The rhythm set the shape of each
day and the work set its content, which is a smaller and odder difference than it sounds.

Every problem this week found was found by using a spec, and none by reading one. The handoff conflict
sat in two files from the day the queue SOP shipped on Day 025 until Day 029, and in that window it
passed a weekly map and the reflect after it, both written with those records in hand. Neither turned it
up. Twelve invented rows found it in an afternoon, at the moment two rows three apart had to be written
differently: the same build coming back with new work gets its own row, and the same build coming back
after a send-back does not. Reading a spec asks whether it makes sense. Filling it in asks it a question
it has to answer, and only the second one is a test. That cuts back at me as well. I wrote the rows and
the specs both, so the use was sympathetic, and most of the awkward cases in that log are ones the specs
had already anticipated, because the same head anticipated them. One case was not anticipated, and that
one is the whole yield. Somebody writing rows they cared about against definitions they did not author
would produce that kind at a rate a single author cannot fake.

The sharpest single day was the one where the right answer was to build nothing. The Analyze slot puts a
quiet pressure on me to produce a number, and an easy fifth metric was sitting there, some rate of the
index's pointers that still resolve, whose only acceptable value is 100 percent. Every other number in
that folder stands in for something nobody can read directly, and week 4's log already spent a paragraph
on what that costs them. Index staleness has its ground truth sitting in the same directory. A path
resolves or it does not. A version claim matches an H1 or it does not. Estimating that costs the same
exhaustive read and hands back a percentage in place of the two file names that failed. Measure what you
must estimate, test what you can decide. Refusing the number was a real output of the day, since adding
it would have been the easy way to fill the slot. Writing the map the next morning gave me words for
what that refusal changed. Weeks 2, 3, and 4 each closed through a number pointing back at one earlier
stage. This one closes through editing, triggered by the act of changing anything, and a maintenance
loop fires when somebody changes a file, not when somebody reads a chart.

## What was thinner than I wanted

The records are authored, and by the person who wrote the definitions they exercise. Twelve log rows and
four waiting builds invented in an afternoon show that the three metrics compute and say nothing about a
real queue: the 19-day wait, the false approval, and the 25 percent send-back rate are all numbers I
chose the inputs for. The ruling has met exactly one case, the one that produced it. The write-time
guide has been run against no rows at all, so its four steps and its fail-safe are a habit described and
not a habit anyone has, the same way week 4's reviewer guide has onboarded nobody.

The check is the thinnest piece of all, because running is the whole of its value. It specifies four
rules and this repo has shipped no code, so it exists as a paragraph. It was run once by hand on the day
the index shipped, 22 paths and 24 version claims, zero mismatches, which is a datapoint and not a
habit. A specified check nobody runs catches exactly as much as no check, which is the same shape as the
log nobody keeps, and I have now written both.

The maps now have the problem they spent the week naming. Five weekly maps sit in `integration/` and
nothing indexes them. Day 032's index lists three of them as background and has never heard of week 5's,
so that map is the second unindexed file in the tree, after the memo that named the rule which would
flag it. That rule has never been run either, since the one hand pass predates it and read paths and
versions only. Under all of it, same as the last four weeks, none of this has run with real people: no
queue anyone pulled from, no build handed to a second person, no audit by a third.

The week's own finding is a sample of one, and it is the claim in here I am least entitled to. One
person wrote every file in this repo, so a problem the system handed me and a problem I went looking for
are the same act seen from two sides, and a single week cannot tell them apart. Week 6 either generates
its own agenda the same way or the claim was a coincidence with a good name on it.

## Carrying into week 6

- Run the check instead of describing it. Four rules, 22 paths, 24 version claims, and no code in the
  repo to run them, so this is where the specification either becomes a habit or stays a paragraph.
- Index the five weekly maps in `integration/`, since nothing indexes them and the newest one is a file
  the index has never heard of.
- Keep naming the standing gap from week 3: none of this has run with real people, and every record in
  it was written by the person who wrote the spec behind it.

The streak is at thirty-four days. More useful than the number is that I picked almost none of the
subjects that went into this one. Four of the five weekday artifacts answered a problem the day before
had made, which is the first evidence that what is written here is being kept and not only added to.
