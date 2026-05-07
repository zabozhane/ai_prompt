from pathlib import Path

from ai_context.llm.client import LLMClient
from ai_context.schemas.project import ProjectSpec
from ai_context.settings import Settings
from ai_context.utils.prompt_loader import PromptLoader


class SpecGenerator:
    def __init__(self, settings: Settings) -> None:
        self._llm = LLMClient(settings)
        prompts_dir = Path(__file__).resolve().parent.parent / "prompts"
        self._prompts = PromptLoader(prompts_dir)

    def generate(self, *, project_idea: str, preferred_stack: str, constraints: list[str]) -> ProjectSpec:
        system = self._prompts.load_text("spec.system.txt")
        user = self._prompts.render_text(
            "spec.user.txt",
            {
                "project_idea": project_idea,
                "preferred_stack": preferred_stack,
                "constraints": constraints,
            },
        )
        return self._llm.generate_structured(system=system, user=user, schema=ProjectSpec)
