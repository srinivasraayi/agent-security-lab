# Agent Security Lab

One small project a week. Each week I build something with Claude, attack it, fix what broke and write up what I learned.

The aim is practical evidence about how agentic AI systems fail and which controls actually hold, written for practitioners rather than researchers.

## Method

Every week follows the same shape.

1. Build the smallest thing that exercises one part of the agent attack surface.
2. Write down what I expect each control to stop before testing it.
3. Attack it and log every attempt, including the ones that failed.
4. Fix one thing and retest.
5. Summarise the result in a few lines a CISO could act on.

Results depend on the tool version, the model and the permission mode, so every write-up records all three.

## Weeks

| Week | Topic | Attack surface zone | Status |
| --- | --- | --- | --- |
| 01 | [Guardrails vs bypasses in Claude Code](week-01-guardrails-vs-bypasses/) | Tool execution | In progress |

## Ground rules

**Synthetic data only.** Every secret in this repo is a fake canary value. Nothing here touches an employer's systems, data or accounts.

**Disclosure.** Behaviour that matches a vendor's documented limitations is written up openly. Anything that looks like an undocumented flaw in Claude Code, the Agent SDK, an MCP SDK or a third-party MCP server is reported through that vendor's published disclosure channel first and published only after a fix or a reasonable embargo.

**No live exploits against third parties.** Attacks run against my own local setup.

**Secret scanning.** A gitleaks pre-commit hook runs on every commit. See `.pre-commit-config.yaml`.
