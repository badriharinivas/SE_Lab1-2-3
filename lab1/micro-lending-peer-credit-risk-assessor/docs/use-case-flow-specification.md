# Use-Case Flow Specification

## Use Case: Calculate Borrower Credit Risk

| Field | Detail |
|---|---|
| **Use Case ID** | UC-02 |
| **Use Case Name** | Calculate Borrower Credit Risk |
| **Primary Actor** | Borrower (initiates via profile submission or loan request) |
| **Secondary Actor(s)** | Peer Lender (consumer of the resulting risk rating) |
| **Description** | Computes a heuristic credit risk rating (Low / Medium / High) for a Borrower using their financial profile, repayment history, and employment stability, so that Peer Lenders can make informed funding decisions. |
| **Trigger** | A Borrower submits or updates their financial profile, or initiates a new loan request that requires a current risk rating. |

### Preconditions

1. The Borrower has an active account on the platform.
2. The Borrower has submitted a financial profile containing income, existing debt, and employment details (FR-001).
3. The risk-scoring rule set (weights and thresholds, per the Assumptions and Business Rules) is configured in the system.

### Postconditions

1. A risk rating (Low / Medium / High) has been computed and associated with the Borrower's current financial profile.
2. The computed risk score and category are persisted and timestamped.
3. The risk rating is visible to the Borrower and to any Peer Lender viewing that Borrower's loan requests.

### Main Success Scenario

1. Borrower submits or updates their financial profile (or initiates a loan request referencing their existing profile).
2. System validates that all required financial profile fields (income, existing debt, employment status, employment duration) are present and well-formed.
3. System retrieves the Borrower's platform repayment history (or applies the "new borrower" default if none exists).
4. System calculates the Debt-to-Income Score from monthly income and existing debt obligations.
5. System calculates the Repayment History Score from the retrieved repayment history.
6. System calculates the Employment Stability Score from employment status and duration.
7. System combines the three sub-scores using the defined weighted formula to produce a single Risk Score (0–100).
8. System maps the Risk Score to a risk category (Low / Medium / High) using the defined thresholds.
9. System stores the Risk Score, category, and timestamp against the Borrower's profile.
10. System displays the risk rating to the Borrower and makes it available to Peer Lenders on any associated loan request.

### Alternate Flows

**A1 — Incomplete Financial Profile**
Trigger: At step 2, the system detects that one or more required financial profile fields are missing.
1. System halts the calculation and does not produce a risk rating.
2. System displays a validation message to the Borrower identifying the missing field(s).
3. System prompts the Borrower to complete their profile before a risk rating can be generated.
4. Use case ends without a rating being stored (system does not default to an approval).

**A2 — Invalid Financial Values**
Trigger: At step 2, a submitted value is present but invalid (e.g., negative income, non-numeric debt figure).
1. System rejects the specific invalid field with a descriptive error message.
2. System retains the previously valid profile data, if any, without overwriting it with invalid input.
3. Borrower is prompted to correct and resubmit the value.
4. Use case resumes at step 2 once corrected data is submitted.

**A3 — No Prior Repayment History (New Borrower)**
Trigger: At step 3, the Borrower has no prior loans on the platform.
1. System applies the default neutral Repayment History Score (70) instead of failing.
2. Use case continues normally from step 4.
