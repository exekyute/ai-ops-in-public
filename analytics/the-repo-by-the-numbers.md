# The Repo by the Numbers (v1)

Forty-six days of files here describe how a review loop should work. None of them ever counted the tree they sit in. This one does, as of 2026-08-07.

[Measure or Test](measure-or-test.md) set the rule: measure what you must estimate, test what you can decide. Counts taken off a directory are decidable, so a file that asserted its own counts would be asking for trust it does not need. Every figure below carries the command that produces it, runnable from the repo root after a clone. The CI line is the one exception, and it says so where it appears.

Three notes on method. `private/` is gitignored, so the commands exclude it. Word counts come from Python's `str.split()`, so match that definition before comparing. These counts predate this file and its entry, so running the commands on a current clone returns more than the tables show, and by more than two where this file is dense with what it counts: it adds a versioned living document, its own links, and its own words. Check out the commit before this one to reproduce the tables exactly.

## Thirty-four living documents, seven revisions

```sh
python -c "import pathlib,re;L=set();V=set();[( V.add(str(p)) if re.search(r'^# .+\(v\d+\)\s*$',t:=p.read_text(encoding='utf-8'),re.M) else None, L.add(str(p)) if re.search(r'^\*v\d+\. A living',t,re.M) else None) for p in pathlib.Path('.').rglob('*.md') if 'private' not in p.parts];print(len(V),len(L),V^L)"
grep -rhoE '^# .+\(v[0-9]+\)$' --include='*.md' --exclude-dir=private . | grep -oE 'v[0-9]+' | sort | uniq -c
grep -rlE '^# .+\(v[2-9]\)$' --include='*.md' --exclude-dir=private .
grep -rhE '^\*v[0-9]+\. A living' --include='*.md' --exclude-dir=private . | grep -icE 'next pass|later pass'
```

| Claim | Count |
| --- | ---: |
| Files closing as a living document | 34 |
| Of those, naming what the next pass does | 24 |
| Files ever revised | 7 |

The first command prints an empty set: a versioned title and a living footer always travel together, so both 34s are the same 34 files. Of those, 27 sit at v1, 5 at v2, none at v3, and 2 at v4. The third command names the seven that ever left v1:

- [Metric Definitions](metric-definitions.md) (v4)
- [The Review Log](../sops/review-log-spec.md) (v4)
- [Automation Standards](../standards/automation-standards.md) (v2)
- [AI Build Review Checklist](../governance/ai-build-review-checklist.md) (v2)
- [SOP: Run a Build Review](../sops/run-a-build-review.md) (v2)
- [SOP: Run the Review Queue](../sops/run-the-review-queue.md) (v2)
- [Checks](../checks/README.md) (v2)

A living document that never moved is a label doing no work.

The raw ratio needs a correction. 7 of 34 does not control for age, and this repo added roughly a file a day, so the v1 pile is full of files too young to have been revised. Eight of the 27 are under ten days old, and one is a day old. Split the 34 by the date each file was added:

```sh
for f in $(grep -rlE '^# .+\(v[0-9]+\)$' --include='*.md' --exclude-dir=private .); do echo "$(git log --diff-filter=A --format=%ad --date=short -- $f | tail -1) $f"; done | sort
```

| Cohort | Revised | Total | Rate |
| --- | ---: | ---: | ---: |
| Added over 30 days ago | 4 | 11 | 36% |
| Added 30 days ago or less | 3 | 23 | 13% |

Median age is 42 days for a revised file and 18 for an unrevised one. The neglect is real but smaller than 7 of 34 makes it look, and a daily cadence pays for new files in a way it never pays for a second pass at an old one.

The seven that moved are the load-bearing ones, the files a person follows or is judged against. Exposure is the pattern, though it does not explain everything. [Tool Adoption Stages](../enablement/tool-adoption-stages.md) is the second-oldest artifact and a guide people follow, and it never left v1. Neither did [the builder self-check](../enablement/builder-self-check.md) at 37 days. Old and followed was not sufficient. Old and argued with was.

Revision also pooled. Nothing sits at v3, and the two at v4 went around three times each while nothing else reached a second pass.

[Maintenance Policy](../governance/maintenance-policy.md) already settled how to read those closing lines once the cadence stops: a next-pass line is named open work with nobody assigned to it. The 34 is the size of what that ruling covers. This file ships the thirty-fifth of those footers.

## Size

```sh
python - <<'EOF'
import pathlib, collections
w = collections.Counter(); n = collections.Counter(); each = []
for p in pathlib.Path('.').rglob('*.md'):
    if 'private' in p.parts: continue
    k = p.parts[0] if len(p.parts) > 1 else 'README'
    c = len(p.read_text(encoding='utf-8').split())
    n[k] += 1; w[k] += c; each.append((c, str(p)))
print(sum(n.values()), sum(w.values()))
for k, v in w.most_common(): print(k, n[k], v)
each.sort(); print(each[:4], each[-1])
EOF
```

87 markdown files, 88,799 words.

| Folder | Files | Words |
| --- | ---: | ---: |
| [`daily/`](../daily/) | 46 | 19,953 |
| [`analytics/`](.) | 3 | 10,849 |
| [`integration/`](../integration/) | 6 | 9,596 |
| [`enablement/`](../enablement/) | 7 | 9,509 |
| [`governance/`](../governance/) | 5 | 8,760 |
| [`examples/`](../examples/) | 3 | 8,192 |
| [`log/`](../log/) | 6 | 7,314 |
| [`sops/`](../sops/) | 5 | 7,261 |
| [`standards/`](../standards/) | 2 | 3,072 |
| [`checks/`](../checks/) | 1 | 1,406 |
| [`docs/`](../docs/) | 1 | 1,315 |
| [`automations/`](../automations/) | 1 | 1,039 |
| [README](../README.md) | 1 | 533 |

An artifact runs 1,758 words, a weekly log 1,219, a daily entry 434. The weekly log sits between the two forms because it is written to a deadline like an entry and read like an artifact. `analytics/` averages 3,616 words a file, the densest folder here. Metric Definitions alone runs 5,329 words, more than all of `standards/`. The shortest artifacts are the README at 533, the [automation lifecycle map](../integration/week-01-automation-lifecycle.md) at 548, and Tool Adoption Stages at 583. The shortest files in the tree are early daily entries, the first of them 122 words.

## The format change is visible in the data

```sh
grep -rohF '](' --include='*.md' --exclude-dir=private . | wc -l
grep -rlF '](' --include='*.md' --exclude-dir=private . | wc -l
python -c "import pathlib;[print(p.name, p.read_text(encoding='utf-8').count('](')) for p in sorted(pathlib.Path('daily').glob('*.md'))]"
```

178 markdown links sit in 21 files, leaving 66 of 87 with none. The last command prints the per-entry series, and its shape is a step. Three quarters of the entries carry zero links; the last ten carry 37. The rule was applied from one entry forward and never backdated, so the boundary is a single line in that output.

Of the 66 link-free files, 41 are dated records, the early entries and the weekly logs, and those stay as written. A factual error in one earns a dated note under the claim it corrects, which is what [Maintenance Policy](../governance/maintenance-policy.md) requires. The other 25 are versioned files, and that rule does not cover them. A line in one gets edited when it stops being true.

## How little code there is

```sh
wc -l checks/check_index.py .github/workflows/checks.yml
wc -w checks/README.md checks/check_index.py
python -c "import json;n=json.load(open('automations/handoff-intake/workflow.json'))['nodes'];s=sum('stickyNote' in x['type'] for x in n);print(len(n)-s, s)"
find . -path ./private -prune -o -type f \( -name '*.png' -o -name '*.jpg' -o -name '*.svg' \) -print | wc -l
git log --oneline | wc -l
```

217 lines of Python in [`check_index.py`](../checks/check_index.py). 19 lines of YAML in [the checks workflow](../.github/workflows/checks.yml). One automation, [the handoff intake](../automations/handoff-intake/README.md), which enforces the packet rule at submission time, with 8 working nodes and 3 notes on the canvas. One image in the whole tree. Against 88,799 words.

That ratio is the honest description of the thing: a writing project about operations, whose executable part arrived in the last third. [Checks](../checks/README.md) spends 1,406 words specifying a script of 833. The history says the same. 61 commits between 2026-06-22 and 2026-08-06, 13 of which are not daily entries.

## What the counting cannot see

Word counts measure volume. 5,329 words says nothing about whether the argument inside them holds, and the longest file here could be the weakest.

Version numbers count revisions, which are deliberate acts. A fix that landed without a bump leaves nothing for the tables above to read, so the 7 is a floor.

```sh
gh run list --limit 100 --json conclusion --jq '[.[].conclusion]|group_by(.)|map({(.[0]):length})'
```

CI has run 13 times and every run is green. That command reads GitHub rather than the clone, so it needs `gh` and an authenticated account, and it covers only the weeks since the check was wired up.

The real limit is what nothing here counts: errors that were never found. There is one measured instance. [The log spec](../sops/review-log-spec.md) told readers to keep columns for four required fields after a later version made it five. That line survived seventeen days and two version bumps, in the file the review side reads most often, until it was corrected. The index check could not see it. A file disagreeing with itself in prose is not a claim any of its rules reads. One found error means the tree holds an unknown number of unfound ones.

## Why publish a count at all

Every number above is one command away from being rechecked, including by a reader who expects it to be wrong. That is the reason to publish a count of yourself. An assertion asks to be believed; a command asks to be run. Add a file and the size table moves. Revise one and the seven moves.

---

*v1. A living count. The next pass reruns every command here against a tree that has stopped growing and reports which figures moved.*
