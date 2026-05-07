from ai_context.llm.client import LLMClient
from ai_context.schemas.architecture import ArchitectureSpec
from ai_context.schemas.project import ProjectSpec
from ai_context.settings import Settings


class ArchitectureGenerator:
    def __init__(self, settings: Settings) -> None:
        self._llm = LLMClient(settings)

    def generate(self, spec: ProjectSpec) -> ArchitectureSpec:
        system = (
            "You design lightweight architecture for Python CLI tools. "
            "Prefer explicit modules and deterministic file outputs."
        )
        user = (
            "Design architecture for the following project spec:\n"
            f"{spec.model_dump_json(indent=2)}\n"
            "Return output that fits the ArchitectureSpec schema."
        )
        return self._llm.generate_structured(system=system, user=user, schema=ArchitectureSpec)
