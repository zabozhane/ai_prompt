# ai-context

CLI-first AI context generation tool for AI-assisted software development.

`ai-context` does not generate full production codebases. It generates structured
engineering context artifacts you can use in Cursor and similar IDE workflows.

## What It Generates

- Project specification
- Architecture draft
- Implementation task plan
- Skills and MCP recommendations
- Cursor context artifacts
- Session execution/handoff artifacts
- Workflow quality report

## Core Philosophy

- Filesystem-first
- JSON as source of truth
- Deterministic markdown rendering
- Transparent generation
- Simple, hackable architecture
- No autonomous agent systems

## Quickstart

```bash
cd /project_path
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -e .
cp .env.example .env
# Fill AI_CONTEXT_OPENAI_API_KEY in .env
ai-context init
```

Generate into another folder:

```bash
ai-context init --output-dir "/path/to/project" --create-dir
```

## Generated Output Example

```text
<target-project>/
  .ai/
    project_spec.json
    architecture.json
    tasks.json
    skills.json
    workflow.json

  README.md
  ARCHITECTURE.md
  TASKS.md
  SKILLS.md
  MCP.md
  CURSOR_CONTEXT.md
  CURSOR_EXECUTION_MODE.md
  SESSION_PROMPT.md
  SESSION_HANDOFF.md
  WORKFLOW_REPORT.md
```

## Pipeline

1. Collect input (`idea`, optional `stack/constraints`, output dir)
2. Auto-suggest setup if stack/constraints are missing
3. Generate:
   - `ProjectSpec`
   - `ArchitectureSpec`
   - `TaskList`
   - `SkillsContext` (local packs + LLM fallback)
4. Run workflow consistency checks (`WorkflowAnalyzer`)
5. Save `.ai/*.json` source-of-truth state
6. Render markdown artifacts via Jinja2 templates

## Skills System

Skills are reusable engineering context packs, not agents.

- First, local skill packs are loaded from `src/ai_context/skills/`
- If no relevant pack matches, LLM fallback generates project-specific skills
- Skills include provenance metadata: `source`, `confidence`, `match_reason`

## Workflow Quality Layer

`workflow.json` and `WORKFLOW_REPORT.md` provide lightweight checks for:

- architecture component coverage in tasks
- task dependency integrity
- constraint signal alignment
- overengineering guardrails
- summary quality score

## Prompt Editing

LLM prompts are editable text files in `src/ai_context/prompts/`:

- `setup.system.txt`, `setup.user.txt`
- `spec.system.txt`, `spec.user.txt`
- `architecture.system.txt`, `architecture.user.txt`
- `tasks.system.txt`, `tasks.user.txt`

This lets you tune generation behavior without changing Python orchestration code.

## Recommended Cursor Workflow

In generated projects:

1. Open the project folder in Cursor
2. Ask Cursor to read:
   - `CURSOR_EXECUTION_MODE.md`
   - `SESSION_HANDOFF.md`
   - `.ai/*.json`
3. Execute one task at a time from `TASKS.md`
4. Test each task before moving to the next
5. Update `TASKS.md` and `SESSION_HANDOFF.md` after each completed task

## Environment Variables

Configured via `.env` or environment variables (`pydantic-settings`):

- `AI_CONTEXT_OPENAI_API_KEY` (required)
- `AI_CONTEXT_OPENAI_MODEL` (optional)
- `AI_CONTEXT_TEMPERATURE` (optional)

Never commit real secrets.
