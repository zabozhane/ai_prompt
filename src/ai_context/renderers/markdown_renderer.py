from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from ai_context.schemas.architecture import ArchitectureSpec
from ai_context.schemas.project import ProjectSpec
from ai_context.schemas.skills import SkillsContext
from ai_context.schemas.tasks import TaskList
from ai_context.schemas.workflow import WorkflowSpec


class MarkdownRenderer:
    def __init__(self, templates_dir: Path) -> None:
        self._env = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def _render_file(self, template_name: str, output_path: Path, context: dict) -> None:
        template = self._env.get_template(template_name)
        output_path.write_text(template.render(**context), encoding="utf-8")

    def render_all(
        self,
        *,
        spec: ProjectSpec,
        architecture: ArchitectureSpec,
        tasks: TaskList,
        skills: SkillsContext,
        workflow: WorkflowSpec,
        output_dir: Path,
    ) -> None:
        context = {
            "spec": spec.model_dump(),
            "architecture": architecture.model_dump(),
            "tasks": tasks.model_dump(),
            "skills": skills.model_dump(),
            "workflow": workflow.model_dump(),
        }
        self._render_file("README.md.j2", output_dir / "README.md", context)
        self._render_file("ARCHITECTURE.md.j2", output_dir / "ARCHITECTURE.md", context)
        self._render_file("TASKS.md.j2", output_dir / "TASKS.md", context)
        self._render_file("SKILLS.md.j2", output_dir / "SKILLS.md", context)
        self._render_file("MCP.md.j2", output_dir / "MCP.md", context)
        self._render_file("CURSOR_CONTEXT.md.j2", output_dir / "CURSOR_CONTEXT.md", context)
        self._render_file("SESSION_PROMPT.md.j2", output_dir / "SESSION_PROMPT.md", context)
        self._render_file("WORKFLOW_REPORT.md.j2", output_dir / "WORKFLOW_REPORT.md", context)
