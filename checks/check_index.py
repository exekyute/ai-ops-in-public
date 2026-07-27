"""Check the review-loop index against the tree.

Runs the four rules specified in analytics/measure-or-test.md against
sops/the-review-loop-in-order.md. Standard library only, no dependencies.

    python checks/check_index.py

Exits 0 when every rule passes and 1 when any rule fails, so it can be wired
into whatever runs on a change. Failures print the file names, because the
point of a check is to hand you the thing that broke.
"""

import os
import re
import sys

INDEX = "sops/the-review-loop-in-order.md"

# Scope is a directory list, not a category. A person decided it, which is the
# soft edge measure-or-test.md names: the check is mechanical given a scope.
SCOPED_FOLDERS = [
    "standards",
    "governance",
    "enablement",
    "sops",
    "analytics",
    "integration",
    "examples",
]

# Rule 1 validates any repo path the index cites, including the checker itself.
# Rule 3's scope stays markdown, since it is about review-side artifacts.
PATH_RE = re.compile(r"`([a-z0-9-]+/[a-z0-9._-]+\.(?:md|py))`")
ENTRY_RE = re.compile(r"`([a-z0-9-]+/[a-z0-9._-]+\.md)`, ([^.]+?) \((v\d+)\)")
H1_RE = re.compile(r"^#\s+(.*?)\s+\((v\d+)\)\s*$")
NOT_HERE_RE = re.compile(r"^## Deliberately not here\s*$(.*?)^## ", re.M | re.S)

_ONES = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen",
]
_TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy",
         "eighty", "ninety"]

# Built rather than typed, so the rule does not go red for a reason that is
# not drift once the counts grow past whatever a hand-written list stopped at.
WORDS = {word: n for n, word in enumerate(_ONES)}
for _t in range(2, 10):
    WORDS[_TENS[_t]] = _t * 10
    for _o in range(1, 10):
        WORDS[f"{_TENS[_t]}-{_ONES[_o]}"] = _t * 10 + _o


def as_number(token):
    """Read '18' or 'eighteen' as 18. Returns None if neither."""
    token = token.strip().lower()
    if token.isdigit():
        return int(token)
    return WORDS.get(token)


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def h1_of(path):
    """Return (title, version) from a file's H1, or (None, None)."""
    with open(path, encoding="utf-8") as handle:
        match = H1_RE.match(handle.readline().strip())
    return (match.group(1), match.group(2)) if match else (None, None)


def scoped_files(root):
    found = []
    for folder in SCOPED_FOLDERS:
        directory = os.path.join(root, folder)
        if not os.path.isdir(directory):
            continue
        for name in sorted(os.listdir(directory)):
            if name.endswith(".md"):
                found.append(f"{folder}/{name}")
    return found


def rule_1_paths_resolve(root, index_text):
    """Every path the index cites exists in the tree."""
    cited = sorted(set(PATH_RE.findall(index_text)))
    missing = [p for p in cited if not os.path.isfile(os.path.join(root, p))]
    detail = f"{len(cited)} distinct paths cited"
    return missing, detail


def rule_2_entries_match(root, index_text):
    """Every entry's title and version equal the target file's H1."""
    failures = []
    entries = ENTRY_RE.findall(index_text)
    for path, title, version in entries:
        full = os.path.join(root, path)
        if not os.path.isfile(full):
            continue  # rule 1 already owns this one
        actual_title, actual_version = h1_of(full)
        if actual_title is None:
            failures.append(f"{path}: H1 is not '# Title (vN)'")
        elif (actual_title, actual_version) != (title.strip(), version):
            failures.append(
                f"{path}: index says '{title.strip()} ({version})', "
                f"file says '{actual_title} ({actual_version})'"
            )
    return failures, f"{len(entries)} entry claims checked"


def rule_3_nothing_unindexed(root, index_text):
    """Every in-scope file is cited, excluded on purpose, or is the index."""
    cited = set(PATH_RE.findall(index_text))
    excluded = set()
    section = NOT_HERE_RE.search(index_text)
    if section:
        excluded = set(PATH_RE.findall(section.group(1)))
    unindexed = [
        p for p in scoped_files(root)
        if p != INDEX and p not in cited and p not in excluded
    ]
    detail = f"{len(scoped_files(root))} files in scope, {len(excluded)} excluded on purpose"
    return unindexed, detail


def rule_4_tally_holds(root, index_text):
    """The opening tally recomputes off the tree."""
    cited = set(PATH_RE.findall(index_text))
    section = NOT_HERE_RE.search(index_text)
    excluded = set(PATH_RE.findall(section.group(1))) if section else set()

    counted = [
        p for p in scoped_files(root)
        if p != INDEX and p not in excluded
    ]
    maps = [p for p in counted if p.startswith("integration/")]
    pieces = [p for p in counted if not p.startswith("integration/")]
    folders = sorted({p.split("/")[0] for p in pieces})

    versions = set()
    for path in counted:
        _, version = h1_of(os.path.join(root, path))
        if version:
            versions.add(int(version[1:]))

    claims = [
        (r"(\w+(?:-\w+)?) review-side pieces", len(pieces), "pieces"),
        (r"across (\w+(?:-\w+)?) folders", len(folders), "folders"),
        (r"plus (\w+(?:-\w+)?) weekly maps", len(maps), "weekly maps"),
    ]
    failures = []
    for pattern, actual, label in claims:
        match = re.search(pattern, index_text, re.I)
        if not match:
            failures.append(f"tally: no '{label}' claim found in the opening line")
            continue
        claimed = as_number(match.group(1))
        if claimed is None:
            failures.append(f"tally: cannot read '{match.group(1)}' as a number")
        elif claimed != actual:
            failures.append(f"tally: index says {claimed} {label}, tree has {actual}")

    span = re.search(r"versions from (v\d+) to (v\d+)", index_text)
    if span and versions:
        low, high = f"v{min(versions)}", f"v{max(versions)}"
        if (span.group(1), span.group(2)) != (low, high):
            failures.append(
                f"tally: index says versions {span.group(1)} to {span.group(2)}, "
                f"tree has {low} to {high}"
            )

    detail = f"{len(pieces)} pieces, {len(folders)} folders, {len(maps)} maps"
    return failures, detail


RULES = [
    ("1. every cited path resolves", rule_1_paths_resolve),
    ("2. every entry matches its file's H1", rule_2_entries_match),
    ("3. every in-scope file is indexed", rule_3_nothing_unindexed),
    ("4. the opening tally recomputes", rule_4_tally_holds),
]


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index_path = os.path.join(root, INDEX)
    if not os.path.isfile(index_path):
        print(f"FAIL: cannot find {INDEX}")
        return 1

    index_text = read(index_path)
    print(f"Checking {INDEX}\n")

    failed = 0
    for name, rule in RULES:
        problems, detail = rule(root, index_text)
        if problems:
            failed += 1
            print(f"FAIL  {name}  ({detail})")
            for problem in problems:
                print(f"        {problem}")
        else:
            print(f"pass  {name}  ({detail})")

    print()
    if failed:
        print(f"{failed} of {len(RULES)} rules failed.")
        return 1
    print(f"All {len(RULES)} rules passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
