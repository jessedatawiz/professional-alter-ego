---
name: code-style
description: This project's code-style standard. Apply whenever planning, writing, or modifying code in this repo. Enforces Infrastructure-as-Code orientation, no hardcoded variables, conformance to existing code patterns, minimalistic and performant Pythonic code, and PEP 8 compliance. TRIGGER on any code authoring/editing task and on "plan", "design", "architect", "build", "implement", "refactor".
---

# Project Code Style

These are hard constraints for ALL code produced in this project — whether drafting a plan, writing new code, or modifying existing code. When planning, call these out explicitly so the implementation honors them.

## 1. Infrastructure-as-Code oriented

- Express infrastructure declaratively, not through manual steps or imperative one-off scripts.
- Make everything reproducible and idempotent: running it twice yields the same result.
- Prefer version-controlled, reviewable definitions (e.g. Terraform, Pulumi, CloudFormation, Ansible, Kubernetes manifests, Docker Compose) over click-ops or ad-hoc CLI commands.
- Separate environment-specific configuration from logic so the same code deploys to dev/staging/prod by changing inputs only.

## 2. Never hardcode variables

- No literal secrets, credentials, endpoints, region names, account IDs, ports, paths, or magic numbers embedded in code.
- Source values from environment variables, config files, parameter stores, or IaC variables/inputs.
- Provide sensible, documented defaults where appropriate — but keep them overridable.
- Surface all configurable values at a single, discoverable layer (e.g. a `variables.tf`, a settings module, or a `.env` schema).

## 3. Follow the existing code pattern

- Before writing, inspect the repo: read neighboring files, existing modules, naming conventions, project layout, and dependency/config files.
- Match the established style — directory structure, import ordering, error-handling approach, logging, test layout — rather than introducing a new paradigm.
- Reuse existing utilities, abstractions, and configuration mechanisms instead of duplicating them.
- Only deviate from an existing pattern when there is a clear, stated reason; note it.

## 4. Write minimalistic code

- Solve exactly what the task requires — no speculative features, abstractions, or future-proofing.
- Prefer the smallest correct change. Three clear lines beat a premature abstraction.
- Avoid unnecessary error handling for impossible states; validate only at real boundaries (user input, external APIs).
- No dead code, no commented-out alternatives, no backwards-compat shims unless explicitly required.

## 5. Python: performant and Pythonic

- Use idiomatic constructs: comprehensions, generators, context managers, `enumerate`/`zip`, unpacking, `pathlib`, f-strings, `dataclasses`/`enum` where they fit.
- Prefer built-in data structures and standard-library tools; reach for the right structure (`set`/`dict` for lookups, generators for streaming) for performance.
- Avoid needless copies and O(n²) patterns; stream large data rather than materializing it.
- Use type hints throughout. Favor immutability and pure functions where reasonable.
- Lean on the standard library and well-established packages before writing custom machinery.

## 6. PEP 8 compliance

- Follow PEP 8: 4-space indentation, ~79–99 char lines (match project config), `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants.
- Proper import grouping (stdlib / third-party / local), one statement per line, two blank lines between top-level defs.
- Assume the project's formatter/linter (e.g. `black`, `ruff`, `flake8`) is authoritative — match its config if present.

## How to apply

1. Inspect the repo first to learn existing patterns and config conventions (principle 3).
2. When planning, draft each step to respect these principles and state where configurable values will live (principle 2) and how the work stays IaC-oriented (principle 1).
3. When writing or editing code, keep the change minimal (principle 4) and, for Python, Pythonic and PEP 8-clean (principles 5–6).
