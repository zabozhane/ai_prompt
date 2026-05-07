import re

from ai_context.schemas.architecture import ArchitectureSpec
from ai_context.schemas.project import ProjectSpec
from ai_context.schemas.skills import SkillsContext
from ai_context.schemas.tasks import TaskList
from ai_context.schemas.workflow import (
    WorkflowCheck,
    WorkflowInput,
    WorkflowOutputsSummary,
    WorkflowSpec,
)


class WorkflowAnalyzer:
    """Runs lightweight consistency checks across generated artifacts."""

    def analyze(
        self,
        *,
        project_idea: str,
        preferred_stack: str,
        constraints: list[str],
        spec: ProjectSpec,
        architecture: ArchitectureSpec,
        tasks: TaskList,
        skills: SkillsContext,
    ) -> WorkflowSpec:
        checks: list[WorkflowCheck] = []
        warnings: list[str] = []

        checks.append(self._check_component_task_coverage(architecture, tasks))
        checks.append(self._check_task_dependencies(tasks))
        checks.append(self._check_constraint_signal(constraints, architecture, tasks))
        checks.append(self._check_overengineering_guard(project_idea, constraints, architecture, tasks))

        stack_warning = self._stack_alignment_warning(preferred_stack, skills)
        if stack_warning:
            warnings.append(stack_warning)

        failed_checks = sum(1 for check in checks if not check.passed)
        quality_score = max(0, 100 - failed_checks * 20 - len(warnings) * 5)

        return WorkflowSpec(
            inputs=WorkflowInput(
                project_idea=project_idea,
                preferred_stack=preferred_stack,
                constraints=constraints,
            ),
            checks=checks,
            warnings=warnings,
            outputs_summary=WorkflowOutputsSummary(
                component_count=len(architecture.components),
                task_count=len(tasks.tasks),
                skill_count=len(skills.selected_skills),
            ),
            quality_score=quality_score,
        )

    def _check_component_task_coverage(
        self,
        architecture: ArchitectureSpec,
        tasks: TaskList,
    ) -> WorkflowCheck:
        task_text = " ".join(
            f"{task.title} {task.description}".lower() for task in tasks.tasks
        )
        missing_components = [
            component.name
            for component in architecture.components
            if component.name.lower() not in task_text
        ]
        if missing_components:
            return WorkflowCheck(
                name="component_task_coverage",
                passed=False,
                details=f"No explicit task coverage for components: {', '.join(missing_components)}",
            )
        return WorkflowCheck(
            name="component_task_coverage",
            passed=True,
            details="Each architecture component has explicit task coverage.",
        )

    def _check_task_dependencies(self, tasks: TaskList) -> WorkflowCheck:
        known_ids = {task.id for task in tasks.tasks}
        unknown_dependencies: list[str] = []
        for task in tasks.tasks:
            for dependency in task.depends_on:
                if dependency not in known_ids:
                    unknown_dependencies.append(f"{task.id}->{dependency}")

        if unknown_dependencies:
            return WorkflowCheck(
                name="task_dependency_integrity",
                passed=False,
                details=f"Unknown dependencies found: {', '.join(unknown_dependencies)}",
            )

        return WorkflowCheck(
            name="task_dependency_integrity",
            passed=True,
            details="All task dependencies reference known task IDs.",
        )

    def _check_constraint_signal(
        self,
        constraints: list[str],
        architecture: ArchitectureSpec,
        tasks: TaskList,
    ) -> WorkflowCheck:
        if not constraints:
            return WorkflowCheck(
                name="constraint_signal",
                passed=True,
                details="No constraints provided; check skipped.",
            )

        combined_text = " ".join(
            [
                architecture.overview,
                " ".join(component.name for component in architecture.components),
                " ".join(f"{task.title} {task.description}" for task in tasks.tasks),
            ]
        ).lower()

        missed = []
        for constraint in constraints:
            terms = [term for term in constraint.lower().split() if len(term) >= 5]
            if terms and not any(term in combined_text for term in terms):
                missed.append(constraint)

        if missed:
            return WorkflowCheck(
                name="constraint_signal",
                passed=False,
                details=f"Constraints weakly represented in outputs: {', '.join(missed)}",
            )

        return WorkflowCheck(
            name="constraint_signal",
            passed=True,
            details="Constraints are represented in architecture/tasks text.",
        )

    def _check_overengineering_guard(
        self,
        project_idea: str,
        constraints: list[str],
        architecture: ArchitectureSpec,
        tasks: TaskList,
    ) -> WorkflowCheck:
        banned_terms = [
            "event bus",
            "graph runtime",
            "vector database",
            "microservice",
            "rag",
            "kubernetes",
        ]
        allowed_source = f"{project_idea} {' '.join(constraints)}".lower()
        output_text = " ".join(
            [
                architecture.overview,
                " ".join(component.name for component in architecture.components),
                " ".join(task.title for task in tasks.tasks),
            ]
        ).lower()

        triggered = []
        for term in banned_terms:
            pattern = r"\b" + re.escape(term) + r"\b"
            in_output = re.search(pattern, output_text) is not None
            in_allowed = re.search(pattern, allowed_source) is not None
            if in_output and not in_allowed:
                triggered.append(term)
        if triggered:
            return WorkflowCheck(
                name="overengineering_guard",
                passed=False,
                details=f"Potential overengineering terms detected: {', '.join(triggered)}",
            )
        return WorkflowCheck(
            name="overengineering_guard",
            passed=True,
            details="No overengineering terms detected outside requested scope.",
        )

    def _stack_alignment_warning(self, preferred_stack: str, skills: SkillsContext) -> str | None:
        stack_lower = preferred_stack.lower()
        if not stack_lower:
            return None
        skills_text = " ".join(
            f"{skill.title} {skill.summary} {' '.join(skill.rules)}".lower()
            for skill in skills.selected_skills
        )
        if "python" in stack_lower and "python" not in skills_text:
            return "Preferred stack mentions Python, but skills context has weak Python signal."
        if "windows" in stack_lower and "windows" not in skills_text:
            return "Preferred stack mentions Windows, but skills context has weak Windows signal."
        return None
