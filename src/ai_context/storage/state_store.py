import json
from pathlib import Path

from ai_context.schemas.architecture import ArchitectureSpec
from ai_context.schemas.project import ProjectSpec
from ai_context.schemas.tasks import TaskList


class StateStore:
    def __init__(self, root: Path) -> None:
        self._ai_dir = root / ".ai"
        self._ai_dir.mkdir(exist_ok=True)

    def _write_json(self, filename: str, payload: dict) -> None:
        path = self._ai_dir / filename
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def save_spec(self, spec: ProjectSpec) -> None:
        self._write_json("project_spec.json", spec.model_dump())

    def save_architecture(self, architecture: ArchitectureSpec) -> None:
        self._write_json("architecture.json", architecture.model_dump())

    def save_tasks(self, tasks: TaskList) -> None:
        self._write_json("tasks.json", tasks.model_dump())
