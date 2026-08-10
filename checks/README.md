# Checks (v4)

This folder holds one script. `check_index.py` reads `sops/the-review-loop-in-order.md` and checks
the four rules that `analytics/measure-or-test.md` specified for it on Day 033, which are the
mechanical claims the index makes about the tree around it. The memo closed by admitting that a
specified check nobody runs catches exactly as much as no check, and the week-05 map said the same
thing. The check now exists and has been run.

Run it from the repo root:

```
python checks/check_index.py
```

Python 3, standard library only, nothing to install. Exit 0 means all four rules passed. Exit 1 means
at least one failed, and the failures print under the rule that caught them, naming what broke, which
for the first three rules is a file. The point of a check is to hand you the thing that broke rather
than a score.

## The four rules

1. **Every cited path resolves.** Every backticked `folder/file.md` or `folder/file.py` token in the
   index has to exist in the tree.
2. **Every entry matches its file's H1.** An entry reads as a path, a title, and a version, and the
   title and version together have to equal the H1 of the file the path points at.
3. **Every in-scope file is indexed.** Each `.md` in the seven scoped folders is cited somewhere in
   the index, is named under "Deliberately not here", or fails. The index does not have to cite itself.
4. **The opening tally recomputes.** The counts in the index's first line (pieces, folders, weekly
   maps, version span) get recounted off the tree and compared.

Why each rule exists, why rule 3 is the one that earns its keep, and why this is a check rather than
a fifth entry in `analytics/metric-definitions.md`, are all argued in `analytics/measure-or-test.md`.
This file points at that argument instead of restating it.

## What the first run found

Exit code 1. Two of the four rules failed, and both failures were real drift.

```
pass  1. every cited path resolves  (22 distinct paths cited)
pass  2. every entry matches its file's H1  (24 entry claims checked)
FAIL  3. every in-scope file is indexed  (25 files in scope, 2 excluded on purpose)
        analytics/measure-or-test.md
        integration/week-05-the-loop-gets-kept.md
FAIL  4. the opening tally recomputes  (18 pieces, 6 folders, 4 maps)
        tally: index says 17 pieces, tree has 18
        tally: index says 3 weekly maps, tree has 4

2 of 4 rules failed.
```

Both files rule 3 named had been predicted by name, in writing, before any code existed. Day 033's
memo called itself the twenty-fourth file and the first thing rule 3 would flag, on the day it was
written. Day 034's map called itself the second unindexed file, after the memo that named the rule
which would flag it. The check found those two and nothing else, so the prediction and the catch
match.

Rule 4 failed from the same drift one step along. Two files the index had never heard of are two
files missing from its opening count, one on pieces and one on weekly maps.

The fix was an edit to the index rather than the script. Both files got entries, and the opening line
went to eighteen pieces and four weekly maps. The rerun exited 0.

```
pass  1. every cited path resolves  (25 distinct paths cited)
pass  2. every entry matches its file's H1  (26 entry claims checked)
pass  3. every in-scope file is indexed  (25 files in scope, 2 excluded on purpose)
pass  4. the opening tally recomputes  (18 pieces, 6 folders, 4 maps)

All 4 rules passed.
```

The cited-path count rose by three rather than two because the same pass gave the index a line for
this script, which rule 1 then validated along with everything else.

A check that has only ever passed proves nothing, so three breaks were applied to the index, run, and
reverted. All three exited 1 and named the thing.

- Broke a cited path: rule 1 failed and named `sops/review-log-spec-typo.md`.
- Broke a version claim: rule 2 failed on `analytics/metric-definitions.md`, printing the version the
  index claimed beside the version the file's H1 carries.
- Broke the opening tally: rule 4 failed, reporting a claim of 12 pieces against 18 in the tree.

Rule 3 got no planted break. It had already failed on real drift on the first run, which is a better
demonstration than a synthetic one.

## When to run it

At the moment of the change that would break it: anything added, renamed, or re-versioned on the
review side. The index names that trigger in its own limits, so running the check then costs nothing
beyond what the index already asks for, and the person making the change is the one who knows which
pointers they touched.

This is the write-time principle from `enablement/keeping-the-review-log.md`, where four steps sit in
front of the person before the row is written because that is the only moment the answer is cheap.
Today's run did not follow it. Both files had been unindexed since the day each shipped, three days
for the memo and two for the map, and a late run tells you only how long a pointer was wrong before
anybody looked.

## What it does not check

- **Mechanical claims only.** A path resolving and a version matching say nothing about whether the
  entry's one-line description is still true of the file it points at. A correct pointer into a file
  that quietly changed what it does passes clean, and once the index's version is bumped to match,
  the re-version that made the line untrue is the event rule 2 reports as fine. Meaning, and reading
  order with it, stays a person's job on a cadence.
- **"Indexed" is looser than the rule name.** Rule 3 passes a file whose path appears anywhere in the
  index, including inside another entry's description or in the prose, so a file can satisfy it with
  no entry, no title, and no version claim. Rule 2 only reads entries written as "`path.md`, Title
  (vN)", so an entry in any other shape is skipped rather than failed, which makes "26 entry claims
  checked" a count of the entries that parsed.
- **The scope is a person's list.** The seven folders live in the script and the exclusion section is
  written by hand, so anyone can silence rule 3 on any file by declaring it deliberately not here.
  `checks/` is not one of the seven, so the script is covered only because the index happens to cite
  it, and this file is covered by nothing.
- **Rule 4 reads the tally as written.** The three counts get recomputed and compared. The version
  span is compared only while the opening line still phrases it as "versions from v1 to v4", and a
  rewrap or a reword drops that comparison with no change on screen.
- **CI cannot make anyone read a red build.** A GitHub Actions workflow,
  [checks.yml](../.github/workflows/checks.yml), runs the script on each push and pull request, on a
  weekly schedule, and on demand, so a broken pointer fails the build where anyone can see it. That
  closes the gap the v1 of this file named, that nothing ran the check automatically. What CI cannot do
  is make a person open the result, and the meaning-level drift above stays outside its reach either way.
- **It checks one index.** Every rule reads `sops/the-review-loop-in-order.md` and stops there. Every
  other cross-reference in the repo, and there are many, is still unverified.
- **The schedule expires; the script does not.** GitHub disables scheduled workflows in a public
  repository after sixty days without activity, so on a finished repo the weekly run stops on its own
  and the badge freezes on its last result. Running `python checks/check_index.py` on a clone is the
  version of this check that keeps working.

## What changed in v2

- The check is enforced now. [checks.yml](../.github/workflows/checks.yml) runs it on every push and
  pull request, one day after v1 shipped with "nothing runs it automatically" in its limits. That limit is deleted
  because it stopped being true, and the wiring is recorded in its place.

## What changed in v3

- Added a weekly schedule and a manual trigger to [checks.yml](../.github/workflows/checks.yml). Writing
  [the maintenance policy](../governance/maintenance-policy.md) is what turned this up: the policy leans
  on the check as the one obligation that does not depend on a person remembering, and a workflow
  triggered only by pushes stops firing the moment a repo stops receiving them. Push-only enforcement
  covers a repo under active development and expires exactly when it is needed instead.

## What changed in v4

- Named the schedule's expiry in the limits. A scheduled workflow in a public repository stops firing
  after sixty days without activity, so the CI line above describes a control with an end date, while
  the script it runs has none.
- Corrected this file's own version. The v3 pass bumped the footer and added a changelog entry and left
  the title reading v2, so the file disagreed with itself for six days. Nothing here could have caught
  it: `checks/` sits outside the folders the index check reads, and the check compares an index against
  H1s rather than a file against itself.

---

*v4. A living doc. The next pass records the first drift the check caught that nobody predicted, and
what it would take to point the same four rules at more than one file.*
