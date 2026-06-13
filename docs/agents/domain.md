# Domain Docs

This is a single-context repository. Engineering skills should read the root domain documentation before planning or changing behavior.

## Before exploring, read these

- `CONTEXT.md` at the repo root for project vocabulary.
- `docs/adr/` for architectural and product-boundary decisions that touch the area being changed.
- `AGENTS.md` and `CLAUDE.md` for repository operating guidance.

If a file does not exist, proceed silently. Do not create domain docs upfront; let `/grill-with-docs` create or update them when terms or decisions are resolved.

## Layout

```text
/
|-- CONTEXT.md
|-- docs/
|   |-- adr/
|   `-- agents/
```

## Use the glossary's vocabulary

When output names a domain concept, use the term as defined in `CONTEXT.md`. Do not drift to synonyms the glossary explicitly avoids.

If a concept is missing from the glossary, either avoid inventing new language or note it as a candidate for `/grill-with-docs`.

## Flag ADR conflicts

If an implementation plan, issue, or proposed change contradicts an existing ADR, surface that conflict explicitly instead of silently overriding the decision.
