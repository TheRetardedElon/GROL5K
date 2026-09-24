# ADR-0004: Grok Build is a sandboxed contractor, not an OS owner

- Status: Accepted
- Date: 2026-09-24

## Context

Grok Build is xAI's coding agent (CLI/TUI/ACP/harness). It is useful on a developer workstation and tempting to install on GROL5000 so the household Bot can "just do whatever."

On an appliance, an unsandboxed coding agent is a privileged shell with a cloud loop.

## Decision

1. Grok Bot (`grol-bot`) is the only user-facing agent on GROL5000.
2. Grok Build is never a peer of the Action Broker.
3. The first integration is `grol.build.propose`: drafts only, no apply, no host shell.
4. A later sandbox harness requires its own implementation review and still cannot hold HA or Host API credentials.
5. Using Grok Build to develop this repository on a laptop is out of scope for the OS image.

## Consequences

- Household voice/home-control demos do not wait on Build.
- Script/scene/automation creation stays denied on the AI path until a separate ADR.
- MCP/web_search stay off on the household session even if Build would like them.
