# Agent Harness Template

Starter design for a repository that builds an agent runtime or a multi-agent orchestration system. Copy only the pieces the project will implement, and remove routes to omitted pages from `AGENTS.md`. Replace all example values and verify every command, path, and isolation guarantee in the target environment.

Start with [AGENTS.md](AGENTS.md) as the repository entry point and [HARNESS.md](HARNESS.md) as the runtime contract. The `architecture/` pages own details; keep the entry point short. Use [evals/README.md](evals/README.md) to test behavior, observation quality, isolation, and failure handling.

This template does not require a particular model, framework, sandbox, or agent count. The project must choose those explicitly. If the repository is only an application used by coding agents, use [../repo-spec/README.md](../repo-spec/README.md) instead.
