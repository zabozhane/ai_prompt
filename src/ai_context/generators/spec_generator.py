from ai_context.llm.client import LLMClient
from ai_context.schemas.project import ProjectSpec
from ai_context.settings import Settings


class SpecGenerator:
    def __init__(self, settings: Settings) -> None:
        self._llm = LLMClient(settings)

    def generate(self, *, project_idea: str, preferred_stack: str, constraints: list[str]) -> ProjectSpec:
        system = (
            "You generate concise project specs for CLI-first software tooling. "
            "Avoid overengineering and keep scope realistic for MVP."
        )
        user = (
            f"Project idea: {project_idea}\n"
            f"Preferred stack: {preferred_stack}\n"
            f"Constraints: {constraints}\n"
            "Return output that fits the ProjectSpec schema."
        )
        return self._llm.generate_structured(system=system, user=user, schema=ProjectSpec)
