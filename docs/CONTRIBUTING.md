# Contributing

## Development environment

**Prerequisites:** Python 3.10+, Node.js 20+, [uv](https://docs.astral.sh/uv/)

```bash
# Python
uv sync --dev

# Node (frontend)
npm install
```

Copy the Cesium token file for the frontend:

```bash
cp .env.example .env.local
# edit .env.local to set CESIUM_TOKEN
```

## Available commands

| Command | Ecosystem | Purpose |
|---------|-----------|---------|
| `uv run pytest` | Python | Run all Python tests |
| `uv run python scripts/generate_frontend_catalog.py` | Python | Regenerate satellite JSON from catalog |
| `uv tool install --editable . --force` | Python | Install `aqualord` CLI globally |
| `aqualord opportunities --geo <file> --hours 48 --format json` | Python | Run opportunity query |
| `npm run dev` | Node | Start Next.js dev server (port 3000) |
| `npm run build` | Node | Production build with type checking |
| `npm run lint` | Node | ESLint check |
| `npm test` | Node | Run Vitest test suite |
| `npx tsc --noEmit` | Node | TypeScript type check (no emit) |

## Project structure

```
aqualord/          Python package (catalog, opportunities, TLE fetching)
scripts/           Build and utility scripts
src/               Next.js frontend
  app/api/tle/     API routes (TLE data from CelesTrak)
  domain/          Domain logic (satellite types, orbit math, TLE parsing)
tests/             Python test suite
docs/              Project documentation
  adr/             Architecture Decision Records
```

## Satellite catalog workflow

The Python `mission_catalog.json` is the **single source of truth** for satellite metadata. The frontend JSON is a build artifact, not hand-edited.

**Adding or editing a satellite:**

1. Edit `aqualord/data/mission_catalog.json` (metadata)
2. Edit `aqualord/data/tracking_index.json` (NORAD ID mapping)
3. Edit `aqualord/data/provenance_index.json` (source attribution)
4. Run `uv run pytest` to validate catalog shape
5. Run `uv run python scripts/generate_frontend_catalog.py` to regenerate frontend JSON
6. Run `npx tsc --noEmit` to confirm type compatibility
7. Commit all changed files including the generated JSON

The generate script will:
- Warn on catalog entries that lack a tracking entry (skipped silently)
- Error on unknown sensor modalities (must be added to `SENSOR_TYPE_MAP`)

## Testing

**Python** (pytest, 19 tests):
```bash
uv run pytest
```

Tests cover: catalog validation, provenance index, TLE fetching, CLI integration, and the generate script.

**TypeScript** (Vitest):
```bash
npm test
```

**Type check:**
```bash
npx tsc --noEmit
```

## Code style

Python follows PEP 8. TypeScript follows the conventions defined in `.eslintrc` and Next.js defaults. Run `npm run lint` before opening a PR.

## PR checklist

- [ ] Python tests pass (`uv run pytest`)
- [ ] TypeScript type check passes (`npx tsc --noEmit`)
- [ ] Frontend JSON regenerated if catalog changed
- [ ] No hardcoded secrets or tokens
- [ ] PR references relevant issues
