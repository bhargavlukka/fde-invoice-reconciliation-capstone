# Adoption Strategy

## Phased Rollout
1. **Shadow mode (weeks 1-3):** the tool runs alongside the existing manual process on every in-scope
   invoice, but its verdict is not shown to clerks in real time — it's only compared against actual outcomes
   afterward to validate accuracy before anyone relies on it.
2. **Assisted mode (weeks 4-8):** the tool's extraction and match verdict are shown to the AP clerk as a
   suggestion; the clerk still makes and records the final decision. This is where trust is built.
3. **Limited auto-approval (weeks 9+, only if exit criteria in `scoping/risk_assessment.md` are met):** clean
   matches below the risk threshold are auto-approved; everything else still routes to a human.

## Training
- A short walkthrough for procurement/AP staff covering: what the tool does, what it doesn't do (no
  autonomous payment execution), how to read a flagged discrepancy, and how to override or escalate.
- Documentation pairs every discrepancy type the reconciliation engine can produce with a plain-language
  explanation (reusing the `discrepancies: list[str]` field from the code sample's `MatchResult`).

## Change Management
Addresses each persona's concern directly (per `discovery/interview_notes.md`):
- **CFO:** weekly metrics dashboard (time saved, errors avoided) starting in shadow mode, so ROI evidence
  accumulates before any go/no-go decision.
- **Compliance Officer:** audit log is reviewable from day one of shadow mode, not introduced later.
- **Procurement/AP Lead & clerks:** positioned explicitly as "removes the tedious lookup work, keeps your
  judgment on real exceptions" — never framed as headcount reduction in pilot communications.

## Feedback Loop
Every clerk override of a tool suggestion (assisted mode) is logged with a reason and reviewed weekly; patterns
in overrides feed back into either prompt/logic improvements or golden-dataset additions.
