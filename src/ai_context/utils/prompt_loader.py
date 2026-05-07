from pathlib import Path

from jinja2 import Environment, StrictUndefined


class PromptLoader:
    """Loads and renders prompt templates from the filesystem."""

    def __init__(self, prompts_dir: Path) -> None:
        self._prompts_dir = prompts_dir
        self._env = Environment(undefined=StrictUndefined, autoescape=False)

    def load_text(self, filename: str) -> str:
        path = self._prompts_dir / filename
        return path.read_text(encoding="utf-8").strip()

    def render_text(self, filename: str, context: dict) -> str:
        template_text = self.load_text(filename)
        template = self._env.from_string(template_text)
        return template.render(**context).strip()
