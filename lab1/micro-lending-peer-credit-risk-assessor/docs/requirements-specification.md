# Requirements Specification

**Project:** Micro-Lending & Peer Credit Risk Assessor
**Problem Statement:** #33 — Retail, E-Commerce & Finance
**Assignment:** Software Engineering Lab 1 — Requirements Engineering & UML Use-Case Modelling

## 1. Overview

The Micro-Lending & Peer Credit Risk Assessor is a peer-to-peer micro-finance platform. It allows individual **Borrowers** to submit their financial profiles and request loans, and allows **Peer Lenders** to review borrower risk ratings and fund loan requests. The system computes a transparent, heuristic (rule-based) credit risk rating for each borrower, generates a structured repayment (EMI) schedule once a loan is funded, and monitors repayments to raise automated default warnings when a borrower falls behind.

The system does **not** use machine learning. Risk scoring is performed using a simple, explainable weighted-scoring heuristic, described in the Assumptions and Business Rules section, so that both borrowers and lenders can understand why a rating was assigned.

## 2. Actors

| Actor | Description |
|---|---|
| **Borrower** | An individual seeking a small peer-funded loan. Submits financial profile data, requests loans, views their risk rating, and makes repayments. |
| **Peer Lender** | An individual with capital to lend. Reviews borrower risk ratings and loan requests, funds loans, and monitors repayment/default status on loans they have funded. |

## 3. Functional Requirements

| ID | Description | Priority | Acceptance Criteria | Rationale |
|---|---|---|---|---|
| **FR-001** | The system shall allow a Borrower to register and submit a financial profile consisting of monthly income, existing monthly debt obligations, employment status, and employment duration. | High | **Pass:** A submitted profile with all required fields is stored and retrievable by the borrower and is used in subsequent risk calculations. **Fail:** A profile missing any required field is rejected with a validation message and is not stored. | Accurate, complete financial data is the foundation for any credit risk assessment; incomplete data would make risk scoring meaningless. |
| **FR-002** | The system shall compute a Borrower's credit risk rating (Low / Medium / High) based on debt-to-income ratio, repayment history, and employment stability indicators, using the heuristic scoring rules defined in the Assumptions and Business Rules section. | High | **Pass:** For a borrower with a complete financial profile, the system returns exactly one of Low, Medium, or High, consistent with the defined thresholds. **Fail:** An incomplete financial profile results in a risk rating being generated or a loan being auto-approved without one. | Risk classification is the core value proposition of the platform and directly protects Peer Lenders from uninformed lending decisions. |
| **FR-003** | The system shall allow a Borrower to submit a loan request specifying a requested amount and term, and shall allow a Peer Lender to view the borrower's risk rating and choose to fund that request. | High | **Pass:** A loan request displays the borrower's current risk rating to the Peer Lender before funding is confirmed, and a funded request transitions the loan to a "Funded" state. **Fail:** A loan request can be funded without the risk rating being computed and displayed. | Lenders must be able to make an informed peer-to-peer funding decision based on the borrower's assessed risk. |
| **FR-004** | The system shall automatically generate a structured repayment (EMI) schedule, including due dates and installment amounts, immediately upon a loan being funded. | Medium | **Pass:** A funded loan of amount P and term N produces exactly N installments whose sum equals the total repayable amount (principal plus any interest), each with a distinct due date. **Fail:** A funded loan exists with no repayment schedule, or with installments that do not sum to the total repayable amount. | Borrowers and lenders both require a clear, predictable repayment plan for the loan to be usable in practice. |
| **FR-005** | The system shall monitor repayment status against the generated schedule and automatically trigger a default warning when a scheduled installment is not recorded as paid by its due date. | High | **Pass:** When the current date passes an installment's due date without a recorded payment, a default warning is generated and visible to both the Borrower and the funding Peer Lender within the same day. **Fail:** An overdue, unpaid installment exists with no corresponding default warning. | Early, automated visibility into missed payments is essential for peer lenders to manage risk on an ongoing basis. |

## 4. Non-Functional Requirements

| ID | Type | Description | Priority | Acceptance Criteria | Rationale |
|---|---|---|---|---|---|
| **NFR-001** | Security & Reliability (Transaction Integrity) | All repayment transactions and EMI/payment distribution operations shall be executed within database ACID-compliant transactions (or an equivalent transactional mechanism), ensuring that a repayment is either fully recorded and reflected in the loan balance, or not recorded at all. | High | **Pass:** Under simulated concurrent repayment submissions for the same installment, exactly one payment record is created and the loan balance updates consistently, with no duplicate or partial writes. **Fail:** Any test run produces a double-recorded payment, a duplicate repayment record, or a loan balance inconsistent with recorded payments. | Financial correctness is non-negotiable in a lending platform; a single double-payment or lost-payment bug would break trust in the entire system. |
| **NFR-002** | Performance | The system shall compute and return a Borrower's credit risk rating within 2 seconds of a request being submitted, for at least 95% of requests under normal load (up to 50 concurrent risk-assessment requests). | Medium | **Pass:** Load testing with 50 concurrent risk-assessment requests shows the 95th-percentile response time at or below 2 seconds. **Fail:** More than 5% of requests under the same test exceed 2 seconds. | A responsive risk assessment is necessary so that loan requests and funding decisions are not bottlenecked, keeping the platform usable at a realistic peer-lending scale. |

## 5. Requirements Traceability

| System Feature | Requirement ID(s) |
|---|---|
| Borrower Financial Profile Handling | FR-001 |
| Credit Risk Assessment | FR-002 |
| Loan Request & Funding Interaction | FR-003 |
| Repayment Schedule / EMI Generation | FR-004 |
| Repayment Monitoring & Default Warnings | FR-005 |
| Transaction Integrity & Security | NFR-001 |
| System Responsiveness | NFR-002 |

## 6. Assumptions and Business Rules

These are **project assumptions and simplifications** made for the purposes of an academic Software Engineering assignment. They are not validated financial or regulatory rules and should not be used for real lending decisions.

### 6.1 General Assumptions

1. Each Borrower has exactly one active financial profile at a time; resubmission overwrites the previous profile.
2. A loan request can only be funded in full by a single Peer Lender (no partial/fractional funding) to keep the model simple.
3. Interest is applied as a single flat rate for the purposes of EMI calculation (no compounding), to keep the repayment schedule easy to compute and explain.
4. "Repayment history" for a first-time borrower with no prior loans on the platform is treated as neutral (medium) rather than penalized, to avoid unfairly penalizing new users.
5. All monetary values are handled in a single currency; multi-currency support is out of scope.
6. The system is a single-tenant academic prototype; authentication, KYC/identity verification, and legal loan-agreement enforcement are out of scope beyond what is noted above.

### 6.2 Heuristic Credit Risk Scoring Rules

The risk score is a simple weighted combination of three sub-scores, each normalized to a 0–100 scale:

```text
Risk Score = (0.4 × Debt-to-Income Score)
            + (0.35 × Repayment History Score)
            + (0.25 × Employment Stability Score)
```

**Debt-to-Income (DTI) Score** (lower DTI ratio → higher/better score):
- DTI ≤ 20% → Score = 100
- 20% < DTI ≤ 40% → Score = 70
- DTI > 40% → Score = 30

**Repayment History Score** (based on on-time repayment percentage on the platform; new borrowers default to 70):
- No prior history (new borrower) → Score = 70
- ≥ 90% of past installments paid on time → Score = 100
- 70–89% paid on time → Score = 60
- < 70% paid on time → Score = 20

**Employment Stability Score** (based on employment status and duration):
- Salaried/employed, ≥ 2 years at current employer → Score = 100
- Salaried/employed, < 2 years → Score = 65
- Self-employed / irregular income → Score = 45
- Unemployed / no verifiable income → Score = 10

**Risk Category Thresholds** (final Risk Score is 0–100):
- Risk Score ≥ 75 → **Low Risk**
- 50 ≤ Risk Score < 75 → **Medium Risk**
- Risk Score < 50 → **High Risk**

These weights and thresholds are intentionally simple and explainable so that a rating can be justified to both the borrower and the lender, consistent with the project's transparent, rule-based (non-ML) approach.
