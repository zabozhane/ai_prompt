from pydantic import BaseModel, Field


class WorkflowInput(BaseModel):
    project_idea: str
    preferred_stack: str
    constraints: list[str] = Field(default_factory=list)


class WorkflowCheck(BaseModel):
    name: str
    passed: bool
    details: str


class WorkflowOutputsSummary(BaseModel):
    component_count: int = 0
    task_count: int = 0
    skill_count: int = 0


class WorkflowSpec(BaseModel):
    inputs: WorkflowInput
    checks: list[WorkflowCheck] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    outputs_summary: WorkflowOutputsSummary = Field(default_factory=WorkflowOutputsSummary)
    quality_score: int = 0
