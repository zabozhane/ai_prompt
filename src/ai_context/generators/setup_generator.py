from pathlib import Path

from ai_context.llm.client import LLMClient
from ai_context.schemas.setup import SetupProposal
from ai_context.settings import Settings
from ai_context.utils.prompt_loader import PromptLoader


class SetupGenerator:
    """Suggests stack and constraints when user input is incomplete."""

    def __init__(self, settings: Settings) -> None:
        self._llm = LLMClient(settings)
        prompts_dir = Path(__file__).resolve().parent.parent / "prompts"
        self._prompts = PromptLoader(prompts_dir)

    def propose(
        self,
        *,
        project_idea: str,
        preferred_stack: str | None = None,
        constraints: list[str] | None = None,
    ) -> SetupProposal:
        system = self._prompts.load_text("setup.system.txt")
        user = self._prompts.render_text(
            "setup.user.txt",
            {
                "project_idea": project_idea,
                "preferred_stack": preferred_stack or "not provided",
                "constraints": constraints or [],
            },
        )
        return self._llm.generate_structured(system=system, user=user, schema=SetupProposal)
