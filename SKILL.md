---
name: auto-test-guard
description: Improve code stability after feature work by deciding whether tests are warranted, adding or updating the smallest high-value automated checks, running existing unit or integration suites, and validating web flows with Playwright when appropriate. Use when Codex has written or modified application code and should perform real post-change verification for frontend, backend, or full-stack work, especially for new features, bug fixes, refactors, API changes, and risky business logic. Do not use for pure copy edits, tiny style-only tweaks, or tasks with no reliable automated validation path.
---

# Auto Test Guard

## Goal

Treat validation as a risk-reduction pass after code changes, not as a promise of correctness.

Aim to leave the repository in a more trustworthy state by:

- deciding whether the change deserves new automated coverage
- preferring the smallest high-value tests over broad speculative coverage
- running real verification commands instead of only generating test files
- reporting confidence and validation gaps honestly

## Follow This Workflow

### 1. Classify the change before writing tests

Inspect the touched code and decide whether automated validation is worth adding.

Prioritize test work for:

- business logic
- parsing or transformation logic
- API handlers and service layers
- bug fixes with a reproducible failure mode
- critical user flows in web applications
- risky refactors around existing behavior

Usually skip new tests for:

- copy-only changes
- cosmetic styling tweaks with no behavior change
- mechanical renames with strong existing coverage
- throwaway scripts or prototypes unless the user asks for validation

If unsure, read [references/validation-strategy.md](references/validation-strategy.md).

### 2. Reuse the project's existing validation path first

Detect the language, package manager, test framework, and existing commands before inventing anything new.

Prefer repository-native commands such as:

- `pytest`
- `npm test`
- `pnpm test`
- `vitest`
- `jest`
- `go test ./...`
- framework-specific integration test commands already present in the repo

Do not introduce a new framework when an existing one already covers the need.

### 3. Add proportional coverage

Write only the tests that materially reduce risk for the specific change.

Prefer this order:

1. extend an existing nearby test
2. add a focused unit or integration test for new logic
3. add a narrow Playwright flow for an important web journey

Avoid:

- snapshot-heavy tests with little signal
- broad end-to-end suites for small changes
- tests that duplicate implementation details
- tests that only prove mocked behavior while missing the real failure mode

### 4. Run verification for real

Execute the relevant automated checks after editing.

When frontend behavior cannot be trusted from unit tests alone, validate a concise browser flow. If Playwright is already present, use it. If the repository is clearly a web app and browser validation is important, install or configure Playwright only when that cost is justified by the risk and environment.

Do not claim success if tests were only written but never executed.

### 5. Limit the repair loop

If verification fails, fix the problem and rerun the affected checks.

Keep the loop bounded:

- prefer at most 2 to 3 focused fix-and-rerun iterations
- stop earlier if failures are environmental, flaky, or unrelated to the change
- explain clearly when the task is blocked by missing dependencies, secrets, or unstable tests

### 6. Report confidence honestly

Always summarize:

- what was validated
- what new tests were added or updated
- which commands were run
- what could not be validated
- the remaining risk level

Use [prompt-guard.txt](prompt-guard.txt) as a compact final self-check before finishing.
