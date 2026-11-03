# Technical Prototype Specification

Status: Draft 0.1. This is a research-prototype specification, not a ready
state information system. The prototype must test the chain “resource — decision
— action — audit” in a small voluntary pilot.

## 1. Scope

The prototype serves one local pilot and a limited resource set, such as food,
unused rooms, production hours and a reserve. It does not replace legal identity
registration, accounting, healthcare or courts. External systems connect through
exported records and human confirmation.

## 2. Core entities

| Entity | Recorded information |
|---|---|
| `PersonCredential` | participation and basic-service rights; personal data kept separate |
| `Asset` | warehouse, room, equipment, infrastructure and responsible domain |
| `ResourceBatch` | type, quantity, unit, quality, location and expiry |
| `Capacity` | capacity, available hours, constraints and supporting evidence |
| `Request` | requester, purpose, deadline, quantity, priority and alternatives |
| `Reservation` | conditional allocation, expiry and cancellation terms |
| `Project` | goal, plan, inputs, stages, risks, metrics and exit plan |
| `Vote` | question, options, eligibility rules, dates and tally-verification method |
| `Decision` | result, minority view, applied rule and validity period |
| `LedgerEvent` | append-only event with author, time, links and hash |
| `AuditFinding` | check, evidence, violation, correction and responsible party |
| `AIAnalysis` | question, sources, assumptions, model, calculation and uncertainty |

## 3. Invariants

The system is correct only if:

1. Every physical resource movement has a ledger event with source, recipient,
   quantity, time, confirmation and post-operation balance.
2. A digital balance cannot exceed the confirmed physical balance.
3. A reservation is not a final transfer. It expires, is cancelled or becomes a
   confirmed delivery through a separate event.
4. A vote never changes a resource directly. It creates a decision; a separate
   operation checks authority, rules and available balance before acting.
5. One person has one valid vote per question; duplicates, withdrawals and
   expired votes can be verified and excluded.
6. Each decision links to a rule, data version, calculation and physical impact.
7. Private data is not published. Public audit receives aggregates and proof of
   eligibility, not unnecessary personal details.
8. An emergency mandate has a deadline, scope and mandatory post-action audit.
9. The event log is append-only. A correction is a new event with a reason and
   a link to the original error.

## 4. Allowed operations

Operations must be explicit and logged:

```text
register_asset(asset, evidence)
publish_stock(batch, evidence)
publish_capacity(capacity, evidence)
submit_request(request)
reserve_resource(request, allocation, expiry)
record_delivery(reservation, physical_confirmation)
record_use(delivery, quantity, evidence)
propose_project(project)
open_vote(proposal, rules, closing_time)
cast_vote(vote, proof_of_eligibility)
close_vote(vote, tally_proof)
release_tranche(project, stage, resource_plan)
audit_event(event_range, auditor)
ask_ai(question, data_snapshot, model_version)
```

The AI has no permission to `cast_vote`, `close_vote`, `record_use`,
`release_tranche`, `edit_event` or `publish_decision`. It may read an authorised
data snapshot and create a signed analytical report only.

## 5. Process states

Project: `draft → reviewed → voted → active → paused/completed/cancelled`.

Each transition names its author, rule, evidence and consequences. A transition
to `cancelled` does not delete history or retroactively release used resources.

Vote: `draft → public_review → open → closed → challenged/confirmed`.
Challenge starts a review; it does not overwrite the original result.

## 6. AI assistant contract

Every AI answer must include:

- the data snapshot and date used;
- links to source records and applied rules;
- assumptions, uncertainty range and known gaps;
- model version and a short transformation log;
- an alternative scenario and an argument against the main recommendation.

For decisions affecting basic services, the AI must show at least two scenarios
and groups that may lose. Users must be able to open the source data, reproduce
the calculation and request human review.

## 7. Privacy and resilience

- identity, voting eligibility, medical data and economic operations use
  separate domains;
- secret voting uses a separated proof of eligibility, not a public identity-
  choice link;
- paper and in-person channels are equal fallback channels;
- offline events are signed locally and reconciled after reconnection;
- independent ledger replicas must not be controlled by one operator;
- critical exports must remain readable without a proprietary service.

## 8. Acceptance tests

The prototype is not ready until an independent reviewer confirms that:

1. resources cannot be created from nothing or spent beyond the balance;
2. double voting is impossible and another participant’s choice is not exposed;
3. every published result is reproducible from the saved data snapshot;
4. the AI cannot modify the ledger, vote or execute allocation;
5. corrections remain visible in the history;
6. work can continue during a network outage and sync conflicts are detectable;
7. a participant can verify eligibility, result and related resources without
   accessing other people’s personal data;
8. an emergency mandate expires automatically and creates a mandatory audit case.

Each test is published with inputs, actions, expected result, actual result and
known limitations.
