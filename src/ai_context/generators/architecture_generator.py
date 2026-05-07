from pathlib import Path

from ai_context.llm.client import LLMClient
from ai_context.schemas.architecture import ArchitectureSpec
from ai_context.schemas.project import ProjectSpec
from ai_context.settings import Settings
from ai_context.utils.prompt_loader import PromptLoader


class ArchitectureGenerator:
    def __init__(self, settings: Settings) -> None:
        self._llm = LLMClient(settings)
        prompts_dir = Path(__file__).resolve().parent.parent / "prompts"
        self._prompts = PromptLoader(prompts_dir)

    def generate(self, spec: ProjectSpec) -> ArchitectureSpec:
        system = self._prompts.load_text("architecture.system.txt")
        user = self._prompts.render_text(
            "architecture.user.txt",
            {
                "project_spec_json": spec.model_dump_json(indent=2),
            },
        )
        return self._llm.generate_structured(system=system, user=user, schema=ArchitectureSpec)
