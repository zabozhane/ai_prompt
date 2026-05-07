# ai-context

CLI-first AI context generation tool for AI-assisted software development.

## Quickstart

1. Create and activate a Python 3.12+ virtual environment.
2. Install dependencies:
   - `pip install -e .`
3. Configure environment:
   - `cp .env.example .env`
   - Fill `AI_CONTEXT_OPENAI_API_KEY`
4. Run:
   - `ai-context init`
   - or target another folder: `ai-context init --output-dir /path/to/project --create-dir`
   - stack/constraints can be left empty, then CLI will auto-suggest and ask for confirmation

## Philosophy

- Filesystem-first
- JSON as source of truth
- Deterministic markdown rendering
- Simple, hackable architecture

## Prompt Editing

LLM prompts are stored as editable text files in `src/ai_context/prompts/`:

- `spec.*.txt`
- `architecture.*.txt`
- `tasks.*.txt`
- `setup.*.txt`

Update these files to tune generation behavior without changing Python logic.
