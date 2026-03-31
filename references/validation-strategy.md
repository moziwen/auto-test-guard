# Validation Strategy

Use this file when deciding whether to add tests, which kind to add, how much browser automation is justified, and how to report confidence.

## Decision Rule

Prefer the lightest validation that can realistically catch the most likely regression.

Ask:

1. What behavior changed?
2. What failure would hurt users most?
3. What is the cheapest automated check that would catch that failure?

## When To Add Tests

Add or update tests when the change affects:

- conditional business rules
- data mapping or parsing
- API request or response behavior
- authorization or validation logic
- persistence logic
- bug fixes with a known regression shape
- important user flows such as checkout, login, upload, generation, or save

Usually skip new tests when the change is limited to:

- text or translation copy
- spacing, color, or layout only
- dead-code cleanup with stable surrounding coverage
- generated files that are already covered elsewhere

If the change is small but touches a risky area, still add a targeted test.

## Choose The Test Type

### Prefer unit tests for isolated logic

Use unit tests for:

- pure functions
- business rules
- state transitions
- formatter or parser behavior
- defensive handling of edge cases

These are usually the highest-signal and lowest-cost checks.

### Prefer integration tests for boundaries

Use integration tests for:

- controller plus service behavior
- API contract checks
- ORM or repository logic
- request validation
- serialization and persistence boundaries

Keep mocks minimal. Prefer realistic boundaries over over-mocked green tests.

### Use Playwright only for meaningful web risk

Use Playwright for:

- core page flows that combine UI and network behavior
- regressions that only show up in the browser
- forms, navigation, auth gates, uploads, or multi-step tasks

Keep browser coverage narrow:

- 1 to 2 critical happy paths are better than a large brittle suite
- assert business outcomes, not styling trivia
- prefer stable locators and text with clear intent
- avoid timing-sensitive assertions when a semantic wait is available

Do not add Playwright just because the project has a UI. Add it when browser behavior is part of the risk.

## Discover Existing Commands

Before adding anything new, inspect:

- `package.json` scripts
- `pyproject.toml`
- `pytest.ini`
- `vitest.config.*`
- `jest.config.*`
- framework-specific docs already in the repo
- CI config files that show the intended validation commands

Prefer the command already used by the project or CI.

If there are several options, choose the smallest command that exercises the changed area first, then widen only if needed.

## Installation Heuristics

Install missing validation dependencies only when all of the following are true:

- the repo clearly supports that validation style
- the change is risky enough to justify setup cost
- installation does not conflict with the project's existing tooling
- you can still explain the new dependency clearly

Examples:

- backend repo with existing `pytest` config but missing local packages: install dependencies, then run tests
- web app with existing Playwright config but missing browser binaries: install Playwright and run the narrow flow

Avoid surprising the user with a brand new test stack for a tiny change.

## Repair Loop

After writing or updating tests:

1. run the narrowest relevant command
2. inspect the first real failure
3. fix either code or test, whichever is actually wrong
4. rerun the affected command
5. expand validation only after the narrow check passes

Stop when:

- the remaining failures are unrelated
- the environment is missing secrets, services, or network access
- the suite is flaky and the root cause is outside the task
- more looping would cause broad speculative edits

## Confidence Report Format

End with a compact summary that includes:

- `Validation run:` the commands actually executed
- `Coverage added:` the tests created or updated
- `Not validated:` any areas skipped or blocked
- `Risk:` low, medium, or high with one sentence explaining why

Never imply certainty beyond what was truly exercised.
