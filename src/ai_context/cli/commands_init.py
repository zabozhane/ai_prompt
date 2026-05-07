from pathlib import Path

import typer
from rich import print

from ai_context.generators.architecture_generator import ArchitectureGenerator
from ai_context.generators.setup_generator import SetupGenerator
from ai_context.generators.skills_generator import SkillsGenerator
from ai_context.generators.spec_generator import SpecGenerator
from ai_context.generators.task_generator import TaskGenerator
from ai_context.renderers.markdown_renderer import MarkdownRenderer
from ai_context.settings import get_settings
from ai_context.storage.state_store import StateStore
from ai_context.workflows.workflow_analyzer import WorkflowAnalyzer


def init_command(
    output_dir: Path | None = typer.Option(
        None,
        "--output-dir",
        help="Target directory where .ai state and markdown artifacts will be generated.",
    ),
    create_dir: bool = typer.Option(
        False,
        "--create-dir",
        help="Create --output-dir if it does not exist.",
    ),
) -> None:
    selected_output_dir = output_dir
    if selected_output_dir is None:
        raw_output_dir = typer.prompt(
            "Output directory for generated files",
            default=".",
        )
        selected_output_dir = Path(raw_output_dir)

    project_idea = typer.prompt("Project idea")
    preferred_stack = typer.prompt("Preferred stack (optional)", default="").strip()
    raw_constraints = typer.prompt("Constraints (comma-separated)", default="")
    constraints = [item.strip() for item in raw_constraints.split(",") if item.strip()]

    settings = get_settings()

    setup_generator = SetupGenerator(settings)
    spec_generator = SpecGenerator(settings)
    architecture_generator = ArchitectureGenerator(settings)
    task_generator = TaskGenerator(settings)
    skills_root = Path(__file__).resolve().parent.parent / "skills"
    skills_generator = SkillsGenerator(skills_root=skills_root, settings=settings)

    if not preferred_stack or not constraints:
        proposal = setup_generator.propose(
            project_idea=project_idea,
            preferred_stack=preferred_stack or None,
            constraints=constraints or None,
        )
        proposed_stack = preferred_stack or proposal.preferred_stack
        proposed_constraints = constraints or proposal.constraints

        print("[cyan]Auto-suggested setup:[/cyan]")
        print(f"- preferred stack: {proposed_stack}")
        print(
            "- constraints: "
            + (", ".join(proposed_constraints) if proposed_constraints else "none")
        )

        if typer.confirm("Use this setup?", default=True):
            preferred_stack = proposed_stack
            constraints = proposed_constraints
        else:
            preferred_stack = typer.prompt("Preferred stack", default=proposed_stack).strip()
            edited_constraints = typer.prompt(
                "Constraints (comma-separated)",
                default=", ".join(proposed_constraints),
            )
            constraints = [item.strip() for item in edited_constraints.split(",") if item.strip()]

    spec = spec_generator.generate(
        project_idea=project_idea,
        preferred_stack=preferred_stack,
        constraints=constraints,
    )
    architecture = architecture_generator.generate(spec)
    tasks = task_generator.generate(spec, architecture)
    skills = skills_generator.generate(spec)
    workflow_analyzer = WorkflowAnalyzer()
    workflow = workflow_analyzer.analyze(
        project_idea=project_idea,
        preferred_stack=preferred_stack,
        constraints=constraints,
        spec=spec,
        architecture=architecture,
        tasks=tasks,
        skills=skills,
    )

    root = selected_output_dir.expanduser().resolve()
    if not root.exists():
        if create_dir:
            root.mkdir(parents=True, exist_ok=True)
        else:
            raise typer.BadParameter(
                f"Output directory does not exist: {root}. "
                "Use --create-dir to create it."
            )
    if not root.is_dir():
        raise typer.BadParameter(f"Output path is not a directory: {root}")

    state_store = StateStore(root)
    state_store.save_spec(spec)
    state_store.save_architecture(architecture)
    state_store.save_tasks(tasks)
    state_store.save_skills(skills)
    state_store.save_workflow(workflow)

    templates_dir = Path(__file__).resolve().parent.parent / "templates"
    renderer = MarkdownRenderer(templates_dir)
    renderer.render_all(
        spec=spec,
        architecture=architecture,
        tasks=tasks,
        skills=skills,
        workflow=workflow,
        output_dir=root,
    )

    print("[green]Context generated successfully.[/green]")
    print(f"Output directory: {root}")
    print(f"Workflow quality score: {workflow.quality_score}/100")
    print("JSON state written to .ai/, markdown artifacts rendered successfully.")
