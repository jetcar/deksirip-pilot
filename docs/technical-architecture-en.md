# Technical Architecture for the Pilot

The technical system must make allocation auditable without turning
transparency into total surveillance. It must not make political decisions for
residents or depend on trust in one operator.

## 1. System layers

### 1.1 Identity and rights

- protected proof of identity and participation rights;
- separate credentials for basic services, the social dividend and voting;
- separation of civic identity, medical data and financial records;
- one person, one vote without a single public biometric database;
- offline recovery and access procedures.

### 1.2 Resource register

The register records physical objects as well as money:

- stocks, batches and locations;
- productive capacity and its schedule;
- requests, reservations, deliveries and actual use;
- labor hours, energy, materials and ecological damage;
- the rules used for each calculation.

Every change is a signed event. History must not be silently rewritten. A
blockchain is not required by default: a replicated append-only log with
cryptographic hashes, independent copies and public integrity checks may be
enough.

### 1.3 Economic accounting

For every resource the system should show physical stock, confirmed supply,
reserve, current cost, competing projects, uncertainty and the range of the
estimate. A monetary balance does not replace a physical balance. A project is
not fully funded until people, energy, materials and capacity are visible.

### 1.4 Electronic voting

Voting needs a complete lifecycle: proposal, legal and resource review, public
discussion, independent scenarios, verifiable voting, publication of the result
and consequences, and revision or cancellation under a pre-defined rule.

Sensitive votes need a secret choice, vote verification by the voter and a
verifiable aggregate result without revealing an individual's choice. Paper and
in-person channels must remain available.

### 1.5 AI assistant

The AI may explain calculations, find contradictions, run scenarios, compare
historical and local data, show likely winners and losers, suggest questions
and opposing arguments, and flag weak or incomplete data.

The AI may not vote, alter the register, allocate resources by itself, hide
uncertainty or present a forecast as a fact. Each answer must expose sources,
data date, assumptions, uncertainty range and model version. Important
decisions should use multiple independent models and a human conclusion.

### 1.6 Audit and public verification

The public interface must answer:

> who decided → which rule applied → which data were used → where the physical
> resources went.

Auditors need exportable data, reproducible calculations, independent nodes,
change logs, sampling checks, whistleblower protection and a way to verify
results without access to the operator's private keys.

## 2. Emergency mode

Before launch, define measurable triggers, the temporary mandate, permitted
actions, its expiry, automatic termination and mandatory after-action audit.
Offline events must reconcile with the shared log after connectivity returns.

## 3. Threat model

Test defenses against falsified stock data, duplicate voting, voter coercion,
operator key compromise, manipulated questions or AI evidence, personal-data
leaks, network and power outages, and divergence between the digital register
and physical inventory.

The core principle is that digital transparency should expose mistakes without
allowing one administrator to silently change a decision, resource or history.
