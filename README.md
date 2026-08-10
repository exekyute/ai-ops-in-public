# AI Ops in Public

[![checks](https://github.com/exekyute/ai-ops-in-public/actions/workflows/checks.yml/badge.svg)](https://github.com/exekyute/ai-ops-in-public/actions/workflows/checks.yml)

One real artifact a day for 49 days, 2026-06-22 to 2026-08-09, building a review loop for AI-powered
automation. **Complete and maintained**: the check still runs weekly, and
[the maintenance policy](governance/maintenance-policy.md) says what that means.

New here? [The field guide](FIELD-GUIDE.md) covers the repo in ten minutes, and
[what this repo was](docs/about-this-repo.md) carries the full orientation. What follows is the
framework the run left behind.

---

## One artifact a day: the framework

Daily projects usually fail one of three ways. The days pile up without becoming a thing, the record fills with promises nobody checks, or the cadence trails off with no one ever deciding a last day. The thirteen rules below are what this run set against all three. Some held from the first day. Others were written mid-run, after the failure they now guard against had already cost something. They assume one person and work that is public or could be; nothing in them assumes any particular tool.

### Start

**Pick one system, not a topic.** A topic accepts anything you add to it. A system pushes back: each new piece has neighbors it must agree with, and the places where the pieces refuse to fit are where the real work is.

*[The start-here index](sops/the-review-loop-in-order.md) orders twenty-four pieces of one review loop by when a reader needs each.*

**Fix the kind of artifact in advance and let yesterday pick the subject.** A rotation of kinds, a build one day, a standard or a log another, decides what each day owes; the subject comes from whatever the previous day named as unfinished in its own closing section. The blank page stops arriving, because the backlog gets written in public before you need it.

*[The week 6 log](log/week-06.md) counts a week in which every subject came from a limit an earlier document had named and left unfixed.*

**Write the bar before the work.** Written afterward, a bar describes what you did; written first, it measures it. It will be wrong, and revising it as the system grows around it is the point.

*[The automation standard](standards/automation-standards.md) shipped on the first day, before anything it could judge, and its v2 added the two sections the first week's map of the loop exposed: ownership and rollback.*

### Run

**Ship something complete every day, however small.** Complete means someone else could pick the thing up from what shipped. A small v1 with stated limits does more than a polished fragment, because a fragment cannot be picked up at all.

*Forty-nine days, forty-nine entries in [the daily folder](daily/); [the census](analytics/the-repo-by-the-numbers.md) carries the commands to recount the tree they left behind.*

**Write down every limit and defect you leave in, next to the thing each one describes.** A known defect may stay unfixed; it may not stay unwritten, and it may not hide in a closing disclaimer, where a stack of limits reads as the summary. One bound keeps this from becoming a license: a defect that makes the thing unsafe to run as documented gets the thing marked unfit instead.

*[The handoff automation](automations/handoff-intake/README.md) shipped with four named failures beside its feature list, each with its fix, none of them fixed.*

**Version every document that can change, and make corrections bump the version.** An edit that leaves no trace makes the whole record unreliable, because a reader can no longer tell what stood when. Dated records are the one exception: an error in one earns a dated note under the claim it corrects, since a rewritten record is no longer a record.

*[The review log spec](sops/review-log-spec.md) sits at v4, and its changelog records the repair of an error that had stood for seventeen days.*

**Write for the reader who arrives cold.** Explain each named thing once, where it first appears, and link it. When words keep describing the same structure, draw it, because a diagram has to commit where prose can stay vague.

*[The field guide](FIELD-GUIDE.md) exists because 91,000 words make a poor front door.*

### Check

**Price the enforcement before writing the rule.** Enforcement holds without anyone remembering it, which is a promise no written rule can make. When the check costs less than the paragraph arguing for the rule, skip the paragraph and ship the check.

*A one-screen CI workflow running a single script replaced an index discipline nobody would have kept, recorded in [the check's notes](checks/README.md).*

**Ask what has to keep happening for each control to fire.** Tie a control to an activity and it dies with the activity, silently, because a control that has stopped running looks the same as one with nothing to report.

*This repo's CI fired only on pushes and pull requests, and a finished repo does neither; writing [the maintenance policy](governance/maintenance-policy.md) caught the gap, and the weekly schedule shipped the same day.*

**Publish numbers only with the way to recompute them.** An asserted count asks to be believed; a command asks to be run, including by the reader who expects it to be wrong.

*The figures in [the census](analytics/the-repo-by-the-numbers.md) each carry the command that produces them, and [the closing week's log](log/week-07.md) records the two commands the census draft got wrong, caught by running them.*

**Force your claims narrow enough to check.** Vague claims survive review because nothing in them can be false. Saying exactly what a thing was caught more defects here than the automated checks did.

*[The week 7 log](log/week-07.md) tallies the week in which every closing document found a real defect, in the thing it closed or in its own draft.*

### End

**Name the ending while there is something left to decide.** A thing can be finished as designed long before it is proven in use; stop when the remaining proof has to come from someone other than you. Named ahead of time, an ending turns the final stretch into a deliverable that can be graded against its own promise.

*[The week 6 log](log/week-06.md) set the last day and listed the closing artifacts before any of them had shipped.*

**Leave a policy behind, and tag a final release.** Say in writing what maintained means: which obligations survive the cadence, which improvements create no obligation to act, and what would reopen the work, each naming what it produces. Then close the count and never resume it, because a resumed count turns the ending into a pause.

*[The maintenance policy](governance/maintenance-policy.md) does all of this, and the v1.0.0 tag closes the record.*

Following the four phases buys two things: a finished object instead of an abandoned one, and a record a stranger can verify claim by claim against the files. Nobody has to be in the room to vouch for it. Mid-run, a project on its way to finishing looks exactly like one about to be abandoned; the named ending is what tells a reader which this was.

---

Maintained by Kevin Yu · [github.com/exekyute](https://github.com/exekyute). MIT, see [LICENSE](LICENSE).
