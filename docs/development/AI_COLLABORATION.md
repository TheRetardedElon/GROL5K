# Human + GPT + Grok Collaboration Protocol

GROL5K is intentionally being developed with multiple AI systems and a human project owner.

## Authority

1. The human project owner has final product and merge authority.
2. Repository state outranks chat memory.
3. Accepted ADRs outrank informal proposals.
4. Passing tests outrank confident prose.
5. Current `docs/development/STATUS.md` is the short-form handoff.
6. `GROL_UPSTREAM.md` defines the inherited baseline and sync rules.

## Important upstream distinction

The inherited root `AI_POLICY.md` is Home Assistant / Open Home Foundation policy and remains relevant to any contribution sent back upstream.

GROL5K's own development may use GPT, Grok, and other AI tools extensively, but code still needs review, tests, traceable commits, and understandable reasoning before it is treated as accepted project work.

## Collaboration packet

```text
PROJECT: GROL5K
BRANCH:
HEAD SHA:
MILESTONE:
UPSTREAM BASELINE:
GOAL:
FILES CHANGED:
DECISIONS MADE:
TESTS RUN:
KNOWN FAILURES:
DO NOT CHANGE:
NEXT TASK:
```

## Working rules

- make small reviewable commits
- name the milestone in commit/PR context
- do not silently change compatibility-sensitive HAOS identifiers
- add or update an ADR for architectural changes
- update STATUS.md at milestone transitions
- attach evidence for build/boot claims
- distinguish planned, implemented, and validated
- never claim a physical/VM boot test happened unless it actually ran
- preserve upstream attribution and license files
- do not commit API keys, tokens, certificates, or private signing material

## Suggested division of labor

### Human project owner
Product direction, hardware access, credential provisioning, final UX/behavior acceptance, and real-device observations.

### GPT
Repository architecture, codebase mapping, implementation/review, documentation, CI/test planning, and cross-component integration.

### Grok
xAI/Grok API integration review, Grok-specific runtime behavior, model/tool interaction design, second-pass implementation review, and adversarial review of the agent experience.

The roles are flexible; repository evidence decides correctness.

## Disagreement protocol

1. state the exact disputed claim
2. link the implementation
3. identify a test that distinguishes alternatives
4. run the smallest useful test
5. record the decision if architectural
