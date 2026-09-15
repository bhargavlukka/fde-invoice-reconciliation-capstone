# Stakeholder Map

| Stakeholder | Role | Influence | Primary Concern | Engagement |
|---|---|---|---|---|
| CFO | Executive sponsor | High | Cost savings, ROI, minimal financial risk | Approves budget & go/no-go; reviews business-metric dashboard monthly |
| Compliance Officer | Control owner | High | Auditability, regulatory defensibility, no unreviewed autonomous payments | Approves control design; reviews audit logs; sign-off required before auto-approval threshold changes |
| Procurement / AP Lead | Primary user | Medium-High | Tool doesn't slow the team down, decisions are explainable, doesn't undermine vendor relationships | Daily user of the exception queue; source of UAT feedback; training recipient |
| IT / Security | Gatekeeper | Medium | Data handling, integration risk, LLM-provider exposure | Reviews security plan; approves deployment; owns IAM |
| Accounts Payable Clerks (end users) | Operational user | Medium | Job security / role change, ease of use, trust in the tool's judgment | Shadow-mode observers, later hands-on users |
| Suppliers / Vendors | External, indirect | Low | Faster, more consistent payment; fewer disputes | Indirect beneficiary; not directly engaged in Release 1 |

## Notes
- The CFO and Compliance Officer are joint approvers for the pilot go-live; neither can unilaterally approve.
- The Procurement/AP Lead is the escalation point for any exception the agent cannot resolve.
- IT/Security must sign off on the SharedLLM-gateway data flow before any real invoice data touches the model.
