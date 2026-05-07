from pathlib import Path

from ai_context.schemas.project import ProjectSpec
from ai_context.schemas.skills import SkillPack, SkillsContext


class SkillsGenerator:
    """Infers relevant skills and loads reusable local skill packs."""

    def __init__(self, skills_root: Path) -> None:
        self._skills_root = skills_root

    def generate(self, spec: ProjectSpec) -> SkillsContext:
        available_skills = self._load_skill_packs()
        selected_ids = self._infer_skill_ids(spec, set(available_skills.keys()))
        selected_skills = [available_skills[skill_id] for skill_id in selected_ids]

        return SkillsContext(
            selected_skills=selected_skills,
            selection_rationale=self._selection_rationale(spec, selected_ids),
            mcp_recommendations=self._mcp_recommendations(selected_ids, spec),
        )

    def _load_skill_packs(self) -> dict[str, SkillPack]:
        if not self._skills_root.exists():
            return {}

        packs: dict[str, SkillPack] = {}
        for entry in sorted(self._skills_root.iterdir()):
            if not entry.is_dir():
                continue

            file_map = self._read_skill_files(entry)
            packs[entry.name] = SkillPack(
                id=entry.name,
                title=entry.name.replace("_", " ").title(),
                summary=self._build_summary(file_map),
                prompts=self._extract_points(file_map.get("prompts", "")),
                rules=self._extract_points(file_map.get("rules", "")),
                conventions=self._extract_points(file_map.get("conventions", "")),
                architecture_guidance=self._extract_points(file_map.get("architecture", "")),
                pitfalls=self._extract_points(file_map.get("pitfalls", "")),
                source_files=sorted(file_map.keys()),
            )
        return packs

    def _read_skill_files(self, skill_dir: Path) -> dict[str, str]:
        contents: dict[str, str] = {}
        for file_path in sorted(skill_dir.glob("*.md")):
            contents[file_path.stem] = file_path.read_text(encoding="utf-8")
        return contents

    def _extract_points(self, markdown: str) -> list[str]:
        points: list[str] = []
        for raw_line in markdown.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            if line.startswith(("-", "*")):
                points.append(line[1:].strip())
                continue
            if ". " in line and line[0].isdigit():
                points.append(line.split(". ", 1)[1].strip())
                continue
            points.append(line)
        return points

    def _build_summary(self, file_map: dict[str, str]) -> str:
        available_sections = ", ".join(sorted(file_map.keys()))
        if not available_sections:
            return "Reusable engineering context pack."
        return f"Reusable engineering context pack with: {available_sections}."

    def _infer_skill_ids(self, spec: ProjectSpec, available_ids: set[str]) -> list[str]:
        text = " ".join(
            [
                spec.idea,
                spec.preferred_stack,
                " ".join(spec.constraints),
                " ".join(spec.goals),
            ]
        ).lower()

        selected: list[str] = []
        if "telegram" in text or "bot" in text:
            selected.append("telegram_bot")
        if "async" in text or "asyncio" in text:
            selected.append("python_async")
        if "python" in text and "python_async" not in selected and "python_async" in available_ids:
            selected.append("python_async")

        filtered = [skill_id for skill_id in selected if skill_id in available_ids]
        return list(dict.fromkeys(filtered))

    def _selection_rationale(self, spec: ProjectSpec, selected_ids: list[str]) -> list[str]:
        if not selected_ids:
            return [
                "No matching local skill packs found for this project spec.",
                "Skills can be added by creating folders under src/ai_context/skills/.",
            ]

        reasons: list[str] = []
        for skill_id in selected_ids:
            if skill_id == "telegram_bot":
                reasons.append("Selected telegram_bot because the spec mentions bot/telegram workflows.")
            elif skill_id == "python_async":
                reasons.append("Selected python_async to enforce reliable async patterns in Python services.")
            else:
                reasons.append(f"Selected {skill_id} based on project keywords.")
        return reasons

    def _mcp_recommendations(self, selected_ids: list[str], spec: ProjectSpec) -> list[str]:
        recommendations: list[str] = []

        if "telegram_bot" in selected_ids:
            recommendations.extend(
                [
                    "Telegram Bot API docs/search MCP for quick endpoint lookup.",
                    "HTTP inspection tools (e.g. curl/httpie workflows) to debug webhook/polling flows.",
                ]
            )
        if "python_async" in selected_ids:
            recommendations.extend(
                [
                    "Python docs MCP (asyncio section) for event-loop and coroutine references.",
                    "Package index/search MCP to compare async-ready libraries before adoption.",
                ]
            )

        if "python" in spec.preferred_stack.lower():
            recommendations.append("Ruff + pytest tooling context for fast local feedback loops.")

        # Stable order and dedupe.
        return list(dict.fromkeys(recommendations))
