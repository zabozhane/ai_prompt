from ai_context.llm.client import LLMClient
from ai_context.schemas.setup import SetupProposal
from ai_context.settings import Settings


class SetupGenerator:
    """Suggests stack and constraints when user input is incomplete."""

    def __init__(self, settings: Settings) -> None:
        self._llm = LLMClient(settings)

    def propose(
        self,
        *,
        project_idea: str,
        preferred_stack: str | None = None,
        constraints: list[str] | None = None,
    ) -> SetupProposal:
        system = (
            "You generate pragmatic MVP stack/constraint suggestions for software projects. "
            "Keep recommendations explicit, lightweight, and suitable for a solo engineer."
        )
        user = (
            f"Project idea: {project_idea}\n"
            f"Current preferred stack: {preferred_stack or 'not provided'}\n"
            f"Current constraints: {constraints or []}\n"
            "Return a concise suggested preferred_stack and a short list of constraints."
        )
        return self._llm.generate_structured(system=system, user=user, schema=SetupProposal)
