# Synthesized Interview Notes

These notes synthesize discovery conversations with three representative personas. They are simulated for this
capstone exercise but reflect realistic priorities for each role.

## Persona 1: CFO
**Context:** Owns the P&L impact of AP operations; reports finance metrics to the board.
**Priorities:** Reduce AP headcount-hours spent on manual review; reduce late-payment penalties and duplicate
payments caused by reconciliation errors; a clear ROI story within 2 quarters.
**Fears:** A tool that approves an incorrect payment autonomously and creates a financial-control failure that
surfaces in an audit.
**Representative quote:** *"I don't need this to be magic. I need it to be cheaper and safer than what we do
today, and I need to be able to prove that to the board and to our auditors."*
**Design implication:** No autonomous payment execution in Release 1; ROI must be measurable via time-saved and
error-avoided metrics from day one.

## Persona 2: Compliance Officer
**Context:** Owns SOX-adjacent financial controls and audit readiness.
**Priorities:** Every decision — human or automated — must be traceable: who or what made it, when, and why.
Any automation must have a documented control boundary.
**Fears:** A "black box" approval that an auditor can't reconstruct, or a model that can be prompt-injected
into approving something it shouldn't.
**Representative quote:** *"If I can't show an auditor exactly why an invoice was approved, it doesn't matter
how accurate the tool is — it's a control gap."*
**Design implication:** Full audit logging of every extraction, match decision, and approval; prompt-injection
defenses and a hard approval gate before any action with financial consequence.

## Persona 3: Procurement / AP Lead
**Context:** Manages the day-to-day team that currently does this reconciliation by hand.
**Priorities:** A tool that removes the tedious part of the job (data entry, hunting for documents) without
taking away their judgment on genuinely ambiguous cases; clear reasons when the tool flags something.
**Fears:** Being blamed for a mistake the tool made silently; the team's expertise becoming invisible or
undervalued.
**Representative quote:** *"If it tells me why it flagged something, I'll trust it fast. If it just says
'mismatch' with no explanation, I'll stop using it within a week."*
**Design implication:** Every exception the tool surfaces must include a human-readable discrepancy reason, not
just a boolean flag; rollout should augment the team's workflow, not replace their sign-off.
