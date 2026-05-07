from ai_context.llm.client import LLMClient
from ai_context.schemas.architecture import ArchitectureSpec
from ai_context.schemas.project import ProjectSpec
from ai_context.schemas.tasks import TaskList
from ai_context.settings import Settings


class TaskGenerator:
    def __init__(self, settings: Settings) -> None:
        self._llm = LLMClient(settings)

    def generate(self, spec: ProjectSpec, architecture: ArchitectureSpec) -> TaskList:
        system = (
            "You break software implementation into clear, small tasks for iterative delivery. "
            "Keep tasks practical and dependency-aware."
        )
        user = (
            "Project spec:\n"
            f"{spec.model_dump_json(indent=2)}\n\n"
            "Architecture:\n"
            f"{architecture.model_dump_json(indent=2)}\n"
            "Return output that fits the TaskList schema."
        )
        return self._llm.generate_structured(system=system, user=user, schema=TaskList)
